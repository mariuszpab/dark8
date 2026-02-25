# meta_agent.py
# DARK8 OS — META AGENT: samorozwój kodu + migracje

from dark8_mark01.meta.code_editor import apply_patch, read_code, write_code
from dark8_mark01.migrations.migration_manager import status as migrations_status
from dark8_mark01.migrations.migration_manager import upgrade_all
from dark8_mark01.tools.codegen import generate_code


def meta_analyze(path: str) -> str:
    """
    Analiza kodu — zwraca treść pliku.
    """
    return read_code(path)


def meta_refactor(path: str, instruction: str) -> str:
    """
    Refaktorowanie kodu na podstawie instrukcji w języku naturalnym.
    """
    original = read_code(path)
    if "Plik nie istnieje" in original:
        return original

    prompt = f"""
Zrefaktoruj poniższy kod zgodnie z instrukcją:

Instrukcja:
{instruction}

Kod:
{original}

Wygeneruj kompletną, poprawioną wersję pliku.
"""

    new_code = generate_code(language="python", prompt=prompt)
    return apply_patch(path, new_code)


def meta_extend(path: str, instruction: str) -> str:
    """
    Rozszerzanie kodu — dodawanie nowych funkcji, klas, logiki.
    """
    original = read_code(path)
    if "Plik nie istnieje" in original:
        return original

    prompt = f"""
Rozszerz poniższy kod zgodnie z instrukcją:

Instrukcja:
{instruction}

Kod:
{original}

Wygeneruj kompletną, rozszerzoną wersję pliku.
"""

    new_code = generate_code(language="python", prompt=prompt)
    return apply_patch(path, new_code)


def meta_create(path: str, instruction: str) -> str:
    """
    Tworzenie nowego modułu od zera.
    """
    prompt = f"""
Stwórz nowy moduł zgodnie z instrukcją:

Instrukcja:
{instruction}

Wygeneruj kompletny kod modułu.
"""

    new_code = generate_code(language="python", prompt=prompt)
    return write_code(path, new_code)


def meta_upgrade_dark8_raw() -> str:
    """
    Surowe wykonanie wszystkich migracji — bez pytań.
    Używane tylko po potwierdzeniu w trybie dialogowym.
    """
    return upgrade_all()


def meta_status_dark8() -> str:
    """
    Zwraca status migracji i wersji systemu.
    """
    return migrations_status()
