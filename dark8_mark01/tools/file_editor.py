# file_editor.py
# DARK8 OS — Tools Layer: edycja plików


def append_to_file(path: str, content: str):
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Dodano treść do pliku: {path}"
    except Exception as e:
        return f"Błąd dopisywania do pliku {path}: {e}"


def overwrite_file(path: str, content: str):
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Nadpisano plik: {path}"
    except Exception as e:
        return f"Błąd nadpisywania pliku {path}: {e}"


def read_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Błąd odczytu pliku {path}: {e}"
