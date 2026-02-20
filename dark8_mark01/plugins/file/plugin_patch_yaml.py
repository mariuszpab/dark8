# plugin_patch_yaml.py
import yaml
import os

def handle_PATCH_YAML(task: dict, context: dict) -> dict:
    path = task.get("path")
    patch = task.get("patch")

    if not path:
        return {"error": "PATCH_YAML wymaga pola 'path'"}

    if not isinstance(patch, dict):
        return {"error": "PATCH_YAML wymaga pola 'patch' typu dict"}

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        data = {}

    data.update(patch)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True)

    return {
        "status": "ok",
        "path": path,
        "patched": patch,
    }
