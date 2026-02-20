# plugin_fetch_url.py
from dark8_mark01.utils.dark8_web_fetch import fetch_page
from dark8_mark01.utils.dark8_web_analyze import extract_text_from_html

def handle_FETCH_URL(task: dict, context: dict) -> dict:
    url = task.get("url")
    if not url:
        return {"error": "FETCH_URL wymaga pola 'url'"}

    html = fetch_page(url)
    text = extract_text_from_html(html)

    return {
        "status": "ok",
        "url": url,
        "html": html,
        "text": text,
    }
