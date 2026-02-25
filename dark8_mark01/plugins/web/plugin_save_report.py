# plugin_save_report.py
import os


def handle_SAVE_REPORT(task: dict, context: dict) -> dict:
    path = task.get("path")
    content = task.get("content")

    if not path:
        return {"error": "SAVE_REPORT wymaga pola 'path'"}

    if content is None:
        return {"error": "SAVE_REPORT wymaga pola 'content'"}

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "status": "ok",
        "path": path,
    }
