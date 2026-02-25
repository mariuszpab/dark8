import subprocess
import sys
import tempfile
import os
import locale
from ..command_registry import register_command


def log_info(msg):
    print(f"[INFO][EXEC] {msg}")


def log_error(msg):
    print(f"[ERROR][EXEC] {msg}")


# ---------------------------------------------------------
# SYSTEMOWE KODOWANIE (Windows / Linux / macOS)
# ---------------------------------------------------------

def _get_system_encoding():
    """
    Zwraca preferowane kodowanie systemowe.
    Windows → CP-1250 / CP-852
    Linux/macOS → UTF-8
    """
    enc = locale.getpreferredencoding(False)
    return enc if enc else "utf-8"


# ---------------------------------------------------------
# GŁÓWNY HANDLER
# ---------------------------------------------------------

def handle(command, args, block):
    if command == "RUN":
        return run_command(block)

    if command == "RUN_PYTHON":
        return run_python(block)

    log_error(f"Nieznana komenda EXEC_OPS: {command}")


# ---------------------------------------------------------
# RUN — wykonanie komendy systemowej
# ---------------------------------------------------------

def run_command(cmd_text):
    if not cmd_text:
        log_error("RUN: brak treści komendy.")
        return

    log_info("Wykonywanie komendy systemowej...")

    encoding = _get_system_encoding()

    try:
        result = subprocess.run(
            cmd_text,
            shell=True,
            capture_output=True,
            text=True,
            encoding=encoding,
            errors="replace"
        )

        if result.stdout:
            log_info("OUTPUT:")
            print(result.stdout)

        if result.stderr:
            log_error("ERROR OUTPUT:")
            print(result.stderr)

        log_info(f"Zakończono RUN (kod: {result.returncode})")

    except Exception as e:
        log_error(f"RUN błąd: {e}")


# ---------------------------------------------------------
# RUN_PYTHON — sandbox Python
# ---------------------------------------------------------

def run_python(code):
    if not code:
        log_error("RUN_PYTHON: brak kodu.")
        return

    log_info("Wykonywanie kodu Python...")

    encoding = _get_system_encoding()

    try:
        # Tworzymy tymczasowy plik .py
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py", encoding="utf-8") as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        # Uruchamiamy sandbox
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            encoding=encoding,
            errors="replace"
        )

        if result.stdout:
            log_info("PYTHON OUTPUT:")
            print(result.stdout)

        if result.stderr:
            log_error("PYTHON ERROR:")
            print(result.stderr)

        log_info(f"Zakończono RUN_PYTHON (kod: {result.returncode})")

    except Exception as e:
        log_error(f"RUN_PYTHON błąd: {e}")

    finally:
        # Usuwamy plik tymczasowy
        try:
            os.remove(tmp_path)
        except Exception:
            pass


# ---------------------------------------------------------
# REJESTRACJA KOMEND
# ---------------------------------------------------------

def register():
    for cmd in ["RUN", "RUN_PYTHON"]:
        register_command(cmd, handle)
