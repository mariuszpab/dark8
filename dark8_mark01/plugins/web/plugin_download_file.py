# plugin_download_file.py
from dark8_mark01.utils.dark8_web_fetch import fetch_file


def handle_DOWNLOAD_FILE(task: dict, context: dict) -> dict:
    url = task.get("url")
    if not url:
        return {"error": "DOWNLOAD_FILE wymaga pola 'url'"}

    path = fetch_file(url)

    return {
        "status": "ok",
        "url": url,
        "path": path,
    }
