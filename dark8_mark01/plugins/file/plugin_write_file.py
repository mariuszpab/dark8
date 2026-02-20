# plugin_write_file.py
import os

def handle_WRITE_FILE(task: dict, context: dict) -> dict:
    path = task.get("path")
    content = task.get("content")

    if not path:
        return {"error": "WRITE_FILE wymaga pola 'path'"}

    if content is None:
        return {"error": "WRITE_FILE wymaga pola 'content'"}

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return {
        "status": "ok",
        "path": path,
    }
