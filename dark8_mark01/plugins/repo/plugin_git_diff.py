# plugin_git_diff.py
import subprocess


def handle_GIT_DIFF(task: dict, context: dict) -> dict:
    path = task.get("path")

    if not path:
        return {"error": "GIT_DIFF wymaga pola 'path'"}

    try:
        result = subprocess.run(["git", "-C", path, "diff"], capture_output=True, text=True)
        return {
            "status": "ok",
            "path": path,
            "diff": result.stdout,
        }
    except Exception as e:
        return {"error": f"GIT_DIFF błąd: {e}"}
