# plugin_git_commit.py
import subprocess

def handle_GIT_COMMIT(task: dict, context: dict) -> dict:
    path = task.get("path")
    message = task.get("message")

    if not path:
        return {"error": "GIT_COMMIT wymaga pola 'path'"}

    if not message:
        return {"error": "GIT_COMMIT wymaga pola 'message'"}

    try:
        _add = subprocess.run(
            ["git", "-C", path, "add", "."],
            capture_output=True,
            text=True
        )

        commit = subprocess.run(
            ["git", "-C", path, "commit", "-m", message],
            capture_output=True,
            text=True
        )

        return {
            "status": "ok",
            "path": path,
            "stdout": commit.stdout,
            "stderr": commit.stderr,
        }
    except Exception as e:
        return {"error": f"GIT_COMMIT błąd: {e}"}
