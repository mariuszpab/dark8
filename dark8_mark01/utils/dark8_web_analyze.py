# dark8_web_analyze.py
# Moduł analizy treści internetowych dla DARK8
#
# Funkcje:
# - czyszczenie HTML
# - ekstrakcja tekstu
# - ekstrakcja nagłówków
# - ekstrakcja linków
# - streszczenia
# - słowa kluczowe
#
# Brak limitów rozmiaru i czasu.
# Brak blokad typów danych.
# Pracuje na danych pobranych przez web_fetch.

import re
from collections import Counter

from bs4 import BeautifulSoup

# === CZYSZCZENIE HTML ===


def extract_text_from_html(html: str) -> str:
    """
    Usuwa tagi HTML i zwraca czysty tekst.
    """
    soup = BeautifulSoup(html, "html.parser")

    # usuwamy skrypty i style
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator=" ")

    # czyszczenie białych znaków
    text = re.sub(r"\s+", " ", text).strip()

    return text


# === EKSTRAKCJA NAGŁÓWKÓW ===


def extract_headings(html: str) -> list:
    """
    Zwraca listę nagłówków H1–H6 w kolejności występowania.
    """
    soup = BeautifulSoup(html, "html.parser")
    headings = []

    for level in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        for tag in soup.find_all(level):
            headings.append({"tag": level, "text": tag.get_text(strip=True)})

    return headings


# === EKSTRAKCJA LINKÓW ===


def extract_links(html: str) -> list:
    """
    Zwraca listę linków (href + tekst).
    """
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for a in soup.find_all("a", href=True):
        links.append({"href": a["href"], "text": a.get_text(strip=True)})

    return links


# === STRESZCZENIE TEKSTU ===


def summarize_text(text: str, max_sentences: int = 5) -> str:
    """
    Bardzo prosty algorytm streszczania:
    - dzieli tekst na zdania
    - wybiera pierwsze N
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    summary = " ".join(sentences[:max_sentences])
    return summary.strip()


# === SŁOWA KLUCZOWE ===


def extract_keywords(text: str, top_n: int = 20) -> list:
    """
    Wyciąga najczęściej występujące słowa (prosty algorytm).
    """
    text = text.lower()
    words = re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9]+", text)

    stopwords = {
        "i",
        "oraz",
        "a",
        "w",
        "na",
        "do",
        "z",
        "że",
        "to",
        "jest",
        "się",
        "o",
        "po",
        "nie",
        "tak",
        "jak",
        "ale",
        "dla",
        "tego",
        "co",
        "czy",
        "by",
        "być",
        "ma",
        "od",
        "za",
        "przez",
        "który",
        "która",
        "które",
    }

    filtered = [w for w in words if w not in stopwords]

    counter = Counter(filtered)
    return counter.most_common(top_n)


# === ANALIZA KOMPLEKSOWA ===


def analyze_html(html: str) -> dict:
    """
    Kompleksowa analiza strony:
    - czysty tekst
    - nagłówki
    - linki
    - streszczenie
    - słowa kluczowe
    """
    text = extract_text_from_html(html)

    return {
        "text": text,
        "summary": summarize_text(text),
        "headings": extract_headings(html),
        "links": extract_links(html),
        "keywords": extract_keywords(text),
    }
