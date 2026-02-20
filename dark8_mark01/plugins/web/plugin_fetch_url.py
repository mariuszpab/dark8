# plugin_fetch_url.py
# Plugin FETCH_URL dla DARK8_MARK01
#
# Użycie w .mpx:
# FETCH_URL https://example.com

from dark8_mark01.utils.dark8_web_fetch import fetch_page
from dark8_mark01.utils.dark8_web_analyze import extract_text_from_html


def handle_FETCH_URL(task: dict, context: dict) -> dict:
    """
    task = {
        "type": "FETCH_URL",
        "url": "https://example.com"
    }
    """
    url = task.get("url")
    if not url:
        return {"error": "Brak pola 'url' w zadaniu FETCH_URL"}

    html = fetch_page(url)
    text = extract_text_from_html(html)

    return {
        "status": "ok",
        "url": url,
        "html": html,
        "text": text,
    }
