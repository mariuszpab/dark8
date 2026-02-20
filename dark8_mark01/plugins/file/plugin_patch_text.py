# plugin_patch_text.py
def handle_PATCH_TEXT(task: dict, context: dict) -> dict:
    path = task.get("path")
    find = task.get("find")
    replace = task.get("replace")

    if not path:
        return {"error": "PATCH_TEXT wymaga pola 'path'"}

    if find is None or replace is None:
        return {"error": "PATCH_TEXT wymaga pól 'find' i 'replace'"}

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Nie można odczytać pliku: {e}"}

    new_content = content.replace(find, replace)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return {
        "status": "ok",
        "path": path,
        "replaced": {"find": find, "replace": replace},
    }
