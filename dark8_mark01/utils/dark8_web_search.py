# dark8_web_search.py
# Moduł wyszukiwania informacji dla DARK8
#
# Źródła:
# - DuckDuckGo Instant Answer API (bez klucza)
# - Wikipedia API (bez klucza)
#
# Brak limitów rozmiaru i czasu.
# Brak blokad typów danych.
# Bez scrapowania Google.
# Stabilne, legalne, szybkie.

import requests
from requests.exceptions import RequestException

from dark8_mark01.utils.dark8_security import validate_url_or_raise


# === DUCKDUCKGO SEARCH ===

def search_duckduckgo(query: str) -> dict:
    """
    Wyszukiwanie przez DuckDuckGo Instant Answer API.
    Zwraca dict z informacjami: Abstract, RelatedTopics, URL, Heading.
    """
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"

    validate_url_or_raise(url)

    try:
        response = requests.get(url, timeout=None)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        raise RuntimeError(f"Błąd DuckDuckGo API: {e}")


# === WIKIPEDIA SEARCH ===

def search_wikipedia(query: str, lang: str = "pl") -> dict:
    """
    Wyszukiwanie przez Wikipedia API.
    Zwraca streszczenie i podstawowe dane.
    """
    url = (
        f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/"
        f"{query.replace(' ', '_')}"
    )

    validate_url_or_raise(url)

    try:
        response = requests.get(url, timeout=None)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        raise RuntimeError(f"Błąd Wikipedia API: {e}")


# === WYSZUKIWANIE ŁĄCZONE ===

def web_search(query: str, lang: str = "pl") -> dict:
    """
    Wyszukiwanie łączone:
    1. DuckDuckGo
    2. Wikipedia
    Zwraca połączone wyniki.
    """
    results = {
        "query": query,
        "duckduckgo": None,
        "wikipedia": None,
    }

    # DuckDuckGo
    try:
        results["duckduckgo"] = search_duckduckgo(query)
    except Exception as e:
        results["duckduckgo"] = {"error": str(e)}

    # Wikipedia
    try:
        results["wikipedia"] = search_wikipedia(query, lang=lang)
    except Exception as e:
        results["wikipedia"] = {"error": str(e)}

    return results


# === WYSZUKIWANIE PROSTE (tekstowe) ===

def simple_search(query: str) -> str:
    """
    Zwraca prosty tekstowy wynik wyszukiwania:
    - najpierw Wikipedia
    - potem DuckDuckGo
    """
    # Wikipedia
    try:
        wiki = search_wikipedia(query)
        if "extract" in wiki:
            return wiki["extract"]
    except:
        pass

    # DuckDuckGo
    try:
        ddg = search_duckduckgo(query)
        if ddg.get("Abstract"):
            return ddg["Abstract"]
    except:
        pass

    return f"Brak wyników dla: {query}"
