import subprocess

def run_python(path: str):
    try:
        result = subprocess.run(["python", path], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Błąd uruchamiania: {e}"
