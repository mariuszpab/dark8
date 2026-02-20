# plugin_read_file.py
def handle_READ_FILE(task: dict, context: dict) -> dict:
    path = task.get("path")
    if not path:
        return {"error": "READ_FILE wymaga pola 'path'"}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Nie można odczytać pliku: {e}"}

    return {
        "status": "ok",
        "path": path,
        "content": content,
    }
