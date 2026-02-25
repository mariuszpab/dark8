# plugin_git_clone.py
import subprocess


def handle_GIT_CLONE(task: dict, context: dict) -> dict:
    url = task.get("url")
    dest = task.get("path")

    if not url:
        return {"error": "GIT_CLONE wymaga pola 'url'"}

    if not dest:
        return {"error": "GIT_CLONE wymaga pola 'path'"}

    try:
        result = subprocess.run(["git", "clone", url, dest], capture_output=True, text=True)
        return {
            "status": "ok",
            "url": url,
            "path": dest,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {"error": f"GIT_CLONE błąd: {e}"}
