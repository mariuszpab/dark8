# code_editor.py
# DARK8 OS — META LAYER: edycja i analiza kodu

import os


def read_code(path: str) -> str:
    if not os.path.exists(path):
        return f"Plik nie istnieje: {path}"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Błąd odczytu kodu: {e}"


def write_code(path: str, content: str) -> str:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Zapisano kod do pliku: {path}"
    except Exception as e:
        return f"Błąd zapisu kodu: {e}"


def apply_patch(path: str, patch: str) -> str:
    """
    patch = pełna nowa zawartość pliku
    """
    return write_code(path, patch)
