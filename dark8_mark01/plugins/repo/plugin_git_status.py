# plugin_git_status.py
import subprocess

def handle_GIT_STATUS(task: dict, context: dict) -> dict:
    path = task.get("path")

    if not path:
        return {"error": "GIT_STATUS wymaga pola 'path'"}

    try:
        result = subprocess.run(
            ["git", "-C", path, "status", "--short"],
            capture_output=True,
            text=True
        )
        return {
            "status": "ok",
            "path": path,
            "changes": result.stdout,
        }
    except Exception as e:
        return {"error": f"GIT_STATUS błąd: {e}"}
