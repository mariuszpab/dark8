# plugin_git_pull.py
import subprocess


def handle_GIT_PULL(task: dict, context: dict) -> dict:
    path = task.get("path")

    if not path:
        return {"error": "GIT_PULL wymaga pola 'path'"}

    try:
        result = subprocess.run(["git", "-C", path, "pull"], capture_output=True, text=True)
        return {
            "status": "ok",
            "path": path,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {"error": f"GIT_PULL błąd: {e}"}
