# plugin_analyze_page.py
from dark8_mark01.utils.dark8_web_analyze import analyze_html
from dark8_mark01.utils.dark8_web_fetch import fetch_page


def handle_ANALYZE_PAGE(task: dict, context: dict) -> dict:
    url = task.get("url")
    if not url:
        return {"error": "ANALYZE_PAGE wymaga pola 'url'"}

    html = fetch_page(url)
    analysis = analyze_html(html)

    return {
        "status": "ok",
        "url": url,
        "analysis": analysis,
    }
