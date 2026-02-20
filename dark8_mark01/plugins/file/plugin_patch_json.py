# plugin_patch_json.py
import json
import os

def handle_PATCH_JSON(task: dict, context: dict) -> dict:
    path = task.get("path")
    patch = task.get("patch")

    if not path:
        return {"error": "PATCH_JSON wymaga pola 'path'"}

    if not isinstance(patch, dict):
        return {"error": "PATCH_JSON wymaga pola 'patch' typu dict"}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}

    # aktualizacja
    data.update(patch)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return {
        "status": "ok",
        "path": path,
        "patched": patch,
    }
