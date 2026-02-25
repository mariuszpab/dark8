# plugin_build_project.py
import subprocess


def handle_BUILD_PROJECT(task: dict, context: dict) -> dict:
    path = task.get("path", ".")

    try:
        result = subprocess.run(
            ["python", "setup.py", "build"], cwd=path, capture_output=True, text=True
        )
        return {
            "status": "ok",
            "path": path,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {"error": f"BUILD_PROJECT błąd: {e}"}
