# dark8_network_core.py
# Bezpieczne, ale NIEOGRANICZONE pobieranie danych dla DARK8
#
# Priorytety:
# - brak limitu rozmiaru
# - brak limitu czasu
# - brak blokady binariów
# - pełna swoboda pobierania dużych plików (GB+)
#
# Zabezpieczenia:
# - walidacja URL (z dark8_security)
# - sandbox ścieżek (z dark8_security)
# - obsługa błędów sieciowych
# - logowanie (opcjonalne)

import requests
from requests.exceptions import RequestException

from dark8_mark01.utils.dark8_security import (
    validate_url_or_raise,
    prepare_download_target,
)


# === Pobieranie tekstu / HTML ===

def fetch_text(url: str, encoding: str | None = None) -> str:
    """
    Pobiera stronę jako tekst.
    Brak limitu rozmiaru i czasu.
    """
    validate_url_or_raise(url)

    try:
        response = requests.get(url, timeout=None)  # brak timeoutu
        response.raise_for_status()
    except RequestException as e:
        raise RuntimeError(f"Błąd pobierania URL: {url}\n{e}")

    if encoding:
        response.encoding = encoding

    return response.text


# === Pobieranie JSON ===

def fetch_json(url: str) -> dict:
    """
    Pobiera JSON z internetu.
    Brak limitu rozmiaru i czasu.
    """
    validate_url_or_raise(url)

    try:
        response = requests.get(url, timeout=None)
        response.raise_for_status()
        return response.json()
    except ValueError:
        raise RuntimeError(f"Nie udało się zdekodować JSON z URL: {url}")
    except RequestException as e:
        raise RuntimeError(f"Błąd pobierania JSON: {url}\n{e}")


# === Pobieranie plików (dowolnych, bez limitów) ===

def download_file(url: str, filename: str | None = None, download_dir: str = "dark8_downloads") -> str:
    """
    Pobiera dowolny plik z internetu — bez limitu rozmiaru i czasu.
    Zapisuje go do sandboxa (dark8_downloads).
    Zwraca pełną ścieżkę do zapisanego pliku.
    """
    validate_url_or_raise(url)

    target_path = prepare_download_target(url, filename, download_dir)

    try:
        with requests.get(url, stream=True, timeout=None) as r:
            r.raise_for_status()

            with open(target_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1 MB chunk
                    if chunk:
                        f.write(chunk)

    except RequestException as e:
        raise RuntimeError(f"Błąd pobierania pliku: {url}\n{e}")

    return target_path


# === Pobieranie strumieniowe (np. duże modele AI) ===

def stream_download(url: str, chunk_size: int = 1024 * 1024 * 10):
    """
    Generator strumieniowy — zwraca kolejne fragmenty danych.
    Idealne do pobierania ogromnych plików (GB+).
    """
    validate_url_or_raise(url)

    try:
        with requests.get(url, stream=True, timeout=None) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    yield chunk
    except RequestException as e:
        raise RuntimeError(f"Błąd pobierania strumieniowego: {url}\n{e}")
