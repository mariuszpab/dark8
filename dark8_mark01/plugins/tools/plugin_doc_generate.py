# plugin_doc_generate.py
import subprocess

def handle_DOC_GENERATE(task: dict, context: dict) -> dict:
    path = task.get("path", ".")

    try:
        result = subprocess.run(
            ["sphinx-build", "docs", "docs/_build"],
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
        return {"error": f"DOC_GENERATE błąd: {e}"}
