import sys
import os

from .mpx_parser import parse_mpx_file
from .commands import file_ops, patch_ops, exec_ops, flow_ops
from .plugins import load_plugins


def log_info(msg):
    print(f"[INFO][MAIN] {msg}")


def log_error(msg):
    print(f"[ERROR][MAIN] {msg}")


def main():
    # rejestracja core komend
    file_ops.register()
    patch_ops.register()
    exec_ops.register()
    flow_ops.register()

    # ładowanie pluginów
    load_plugins()

    if len(sys.argv) < 3:
        print("Użycie: python -m dark8_mark01.main run <ścieżka_do_mpx>")
        return

    command = sys.argv[1]
    script_path = sys.argv[2]

    if command != "run":
        log_error(f"Nieznana komenda główna: {command}")
        return

    script_path = os.path.normpath(script_path)

    if not os.path.exists(script_path):
        log_error(f"Plik skryptu nie istnieje: {script_path}")
        return

    log_info(f"Uruchamiam skrypt: {script_path}")

    try:
        parse_mpx_file(script_path)
    except SystemExit as e:
        log_info(f"Skrypt zakończony przez EXIT (kod: {e.code})")
        return
    except Exception as e:
        log_error(f"Nieoczekiwany błąd: {e}")
        return

    log_info("Wykonano cały skrypt MPX.")


if __name__ == "__main__":
    main()
