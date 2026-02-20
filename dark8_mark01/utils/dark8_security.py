# dark8_security.py
# Minimalny, nienarzucający się Security Layer dla DARK8
# Priorytety:
# - BRAK limitu rozmiaru pobierania
# - BRAK limitu czasu pobierania
# - BRAK blokady binariów (.exe, .dll, .sh, itd.)
# - Ochrona przed oczywistymi głupotami (file://, localhost, prywatne IP, ../ poza rootem)
#
# Ten moduł ma chronić przed przypadkowym rozwaleniem systemu,
# ale NIE ma ograniczać samorozwoju, samoaktualizacji ani pracy na dużych plikach.

import os
import re
import ipaddress
from urllib.parse import urlparse


# Katalog sandboxowy na pliki pobierane / tworzone przez DARK8
DEFAULT_DOWNLOAD_DIR = "dark8_downloads"


class SecurityError(Exception):
    """Bazowy wyjątek bezpieczeństwa."""
    pass


class UnsafeURLError(SecurityError):
    """Niebezpieczny lub niedozwolony URL."""
    pass


class UnsafePathError(SecurityError):
    """Niebezpieczna ścieżka pliku."""
    pass


def ensure_download_dir(download_dir: str = DEFAULT_DOWNLOAD_DIR) -> str:
    """
    Upewnia się, że katalog na pobierane pliki istnieje.
    Zwraca absolutną ścieżkę do katalogu.
    """
    abs_dir = os.path.abspath(download_dir)
    os.makedirs(abs_dir, exist_ok=True)
    return abs_dir


# === URL SECURITY ===

def is_safe_url(url: str) -> bool:
    """
    Sprawdza, czy URL jest "sensowny" z punktu widzenia bezpieczeństwa:
    - dozwolone protokoły: http, https
    - brak file://, smb://, ftp://, ssh://, itp.
    - brak localhost / 127.0.0.1 / prywatnych IP
    NIE sprawdza typu pliku, rozmiaru, czasu, binariów, itp.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if parsed.scheme not in ("http", "https"):
        return False

    host = parsed.hostname or ""
    if not host:
        return False

    # localhost / 127.0.0.1 / ::1
    if host in ("localhost", "127.0.0.1", "::1"):
        return False

    # próba interpretacji jako IP
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            return False
    except ValueError:
        # nie jest IP, może być domena – OK
        pass

    return True


def validate_url_or_raise(url: str) -> None:
    """
    Rzuca wyjątek, jeśli URL jest ewidentnie niebezpieczny.
    Nie ogranicza typu pliku, rozmiaru, czasu, binariów.
    """
    if not is_safe_url(url):
        raise UnsafeURLError(f"Niebezpieczny lub niedozwolony URL: {url}")


# === PATH / SANDBOX SECURITY ===

def sanitize_filename(name: str) -> str:
    """
    Proste czyszczenie nazwy pliku:
    - usuwa znaki kontrolne
    - zamienia ścieżki na nazwę (bez katalogów)
    """
    name = name.strip().replace("\0", "")
    name = os.path.basename(name)
    if not name:
        name = "plik"
    return name


def sandbox_path(
    filename: str,
    download_dir: str = DEFAULT_DOWNLOAD_DIR,
) -> str:
    """
    Zwraca BEZPIECZNĄ ścieżkę w katalogu sandboxowym (dark8_downloads).
    Nie pozwala wyjść poza ten katalog (brak ../).
    NIE blokuje nadpisywania plików – to jest świadoma decyzja:
    DARK8 może nadpisywać swoje pliki w ramach samorozwoju.
    """
    base_dir = ensure_download_dir(download_dir)
    safe_name = sanitize_filename(filename)
    full_path = os.path.abspath(os.path.join(base_dir, safe_name))

    # upewniamy się, że ścieżka jest w sandboxie
    if not full_path.startswith(base_dir + os.sep) and full_path != base_dir:
        raise UnsafePathError(f"Ścieżka wychodzi poza sandbox: {full_path}")

    return full_path


def is_path_within_root(path: str, root_dir: str) -> bool:
    """
    Sprawdza, czy ścieżka znajduje się w obrębie root_dir.
    Użyteczne, jeśli chcesz ograniczyć operacje do katalogu projektu.
    """
    abs_root = os.path.abspath(root_dir)
    abs_path = os.path.abspath(path)
    return abs_path.startswith(abs_root + os.sep) or abs_path == abs_root


# === HIGH-LEVEL API ===

def prepare_download_target(
    url: str,
    filename: str | None = None,
    download_dir: str = DEFAULT_DOWNLOAD_DIR,
) -> str:
    """
    Wysokopoziomowa funkcja:
    - sprawdza, czy URL jest bezpieczny (protokół, host)
    - przygotowuje bezpieczną ścieżkę w sandboxie
    - NIE ogranicza rozmiaru, czasu, typu pliku, binariów, archiwów
    Zwraca pełną ścieżkę, do której można zapisać pobierany plik.
    """
    validate_url_or_raise(url)

    if not filename:
        # spróbuj wyciągnąć nazwę z URL
        parsed = urlparse(url)
        candidate = os.path.basename(parsed.path) or "pobrany_plik"
        filename = candidate

    target_path = sandbox_path(filename, download_dir=download_dir)
    return target_path


def can_execute_command(cmd: str) -> bool:
    """
    Minimalna kontrola poleceń systemowych.
    NIE blokuje binariów, NIE blokuje .exe/.dll/.sh.
    Możesz tu dodać własne reguły, jeśli kiedyś uznasz to za potrzebne.
    Na razie – zawsze True.
    """
    # Przykładowo można by blokować ewidentne destrukcyjne komendy typu:
    # if re.search(r"rm\s+-rf\s+/", cmd):
    #     return False
    # Ale zgodnie z Twoimi wytycznymi – nie narzucamy ograniczeń.
    return True


def validate_command_or_raise(cmd: str) -> None:
    """
    Rzuca wyjątek, jeśli komenda jest uznana za niebezpieczną.
    W tej wersji – nic nie blokuje.
    """
    if not can_execute_command(cmd):
        raise SecurityError(f"Komenda zablokowana przez politykę bezpieczeństwa: {cmd}")


# === PODSUMOWANIE ===
#
# Ten moduł robi tylko trzy rzeczy:
# 1. Pilnuje, żeby URL nie był ewidentnie zły (file://, localhost, prywatne IP, złe protokoły).
# 2. Pilnuje, żeby pliki trafiały do sandboxa (dark8_downloads) i nie wychodziły poza niego.
# 3. Daje hooki pod ewentualne przyszłe reguły dla komend systemowych.
#
# NIE:
# - nie ogranicza rozmiaru plików,
# - nie ogranicza czasu pobierania,
# - nie blokuje binariów,
# - nie blokuje .exe, .dll, .sh, .zip, .rar, itd.
#
# To jest wersja zgodna z Twoimi priorytetami: pełna swoboda rozwoju i pracy na dużych plikach,
# przy minimalnej, zdroworozsądkowej ochronie przed oczywistymi pułapkami.
