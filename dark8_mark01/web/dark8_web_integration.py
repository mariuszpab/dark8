# dark8_web_integration.py
# Integracja web_fetch, web_search i web_analyze z DARK8

from dark8_mark01.utils.dark8_web_fetch import (
    fetch_page,
    fetch_file,
)
from dark8_mark01.utils.dark8_web_search import (
    simple_search,
)
from dark8_mark01.utils.dark8_web_analyze import (
    extract_text_from_html,
    analyze_html,
)


# === HANDLERY INTERNETOWE ===

def handle_web_fetch(cmd: str) -> str:
    """
    Pobiera stronę i zwraca czysty tekst.
    """
    # wyciągamy URL z komendy
    parts = cmd.split()
    url = parts[-1]

    html = fetch_page(url)
    text = extract_text_from_html(html)

    return f"=== Zawartość strony: {url} ===\n{text[:5000]}"


def handle_web_download(cmd: str) -> str:
    """
    Pobiera plik i zapisuje go w dark8_downloads.
    """
    parts = cmd.split()
    url = parts[-1]

    path = fetch_file(url)

    return f"Pobrano plik:\n{path}"


def handle_web_search(cmd: str) -> str:
    """
    Wyszukiwanie informacji w internecie.
    """
    query = cmd.replace("wyszukaj", "").replace("search", "").strip()

    results = simple_search(query)

    return f"Wyniki wyszukiwania dla: {query}\n\n{results}"


def handle_web_analyze(cmd: str) -> str:
    """
    Pobiera stronę i wykonuje pełną analizę.
    """
    parts = cmd.split()
    url = parts[-1]

    html = fetch_page(url)
    analysis = analyze_html(html)

    out = []
    out.append("=== STRESZCZENIE ===")
    out.append(analysis["summary"])
    out.append("\n=== SŁOWA KLUCZOWE ===")
    out.append(", ".join([w for w, _ in analysis["keywords"]]))
    out.append("\n=== NAGŁÓWKI ===")
    for h in analysis["headings"]:
        out.append(f"{h['tag'].upper()}: {h['text']}")
    out.append("\n=== LINKI ===")
    for link in analysis["links"][:50]:
        out.append(f"{link['text']} -> {link['href']}")

    return "\n".join(out)
