# dark8_web_fetch.py
# Uproszczona warstwa "Web Fetch" dla DARK8
#
# Korzysta z:
# - dark8_network_core (pobieranie bez limitów)
# - dark8_security (walidacja URL, sandbox ścieżek)
#
# Cel:
# - proste funkcje typu: pobierz stronę, pobierz JSON, pobierz plik
# - gotowe do użycia z UCI / agentem / pluginami

from dark8_mark01.utils.dark8_network_core import (
    download_file,
    fetch_json,
    fetch_text,
    stream_download,
)


def fetch_page(url: str) -> str:
    """
    Pobiera stronę (HTML / tekst) i zwraca jako string.
    """
    return fetch_text(url)


def fetch_api_json(url: str) -> dict:
    """
    Pobiera JSON z API i zwraca jako dict.
    """
    return fetch_json(url)


def fetch_file(url: str, filename: str | None = None, download_dir: str = "dark8_downloads") -> str:
    """
    Pobiera dowolny plik z internetu i zapisuje w katalogu download_dir.
    Zwraca pełną ścieżkę do pliku.
    """
    return download_file(url, filename=filename, download_dir=download_dir)


def fetch_large_file_to(path: str, url: str, chunk_size: int = 1024 * 1024 * 10) -> str:
    """
    Pobiera bardzo duży plik strumieniowo i zapisuje go do podanej ścieżki.
    Użyteczne, gdy chcesz mieć pełną kontrolę nad ścieżką docelową.
    """
    with open(path, "wb") as f:
        for chunk in stream_download(url, chunk_size=chunk_size):
            f.write(chunk)
    return path
