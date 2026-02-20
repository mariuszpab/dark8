# plugin_run_tests.py
import subprocess

def handle_RUN_TESTS(task: dict, context: dict) -> dict:
    path = task.get("path", ".")

    try:
        result = subprocess.run(
            ["pytest", "-q"],
            cwd=path,
            capture_output=True,
            text=True
        )
        return {
            "status": "ok",
            "path": path,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {"error": f"RUN_TESTS błąd: {e}"}
