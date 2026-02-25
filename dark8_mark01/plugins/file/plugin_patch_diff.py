# plugin_patch_diff.py
import difflib

def handle_PATCH_DIFF(task: dict, context: dict) -> dict:
    path = task.get("path")
    diff_text = task.get("content")

    if not path:
        return {"error": "PATCH_DIFF wymaga pola 'path'"}

    if not diff_text:
        return {"error": "PATCH_DIFF wymaga pola 'content' z diffem"}

    try:
        with open(path, "r", encoding="utf-8") as f:
            _original = f.read().splitlines(keepends=True)
    except Exception as e:
        return {"error": f"Nie można odczytać pliku: {e}"}

    diff_lines = diff_text.splitlines(keepends=True)

    patched = list(difflib.restore(diff_lines, 1))

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(patched)

    return {
        "status": "ok",
        "path": path,
    }
