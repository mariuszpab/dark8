import os

from ..command_registry import register_command
from ..mpx_parser import parse_mpx_file


def handle_run_updates(command, args, block):
    """
    RUN_UPDATES
    Uruchamia wszystkie pliki .mpx z katalogu 'updates/' w kolejności alfabetycznej.
    """
    updates_dir = "updates"

    if not os.path.exists(updates_dir):
        print("[UPDATE_SYSTEM] Brak katalogu 'updates/'. Tworzę...")
        os.makedirs(updates_dir, exist_ok=True)
        return

    files = sorted(f for f in os.listdir(updates_dir) if f.endswith(".mpx"))

    if not files:
        print("[UPDATE_SYSTEM] Brak plików aktualizacji w katalogu 'updates/'.")
        return

    print("[UPDATE_SYSTEM] Wykryto aktualizacje:")
    for f in files:
        print(" -", f)

    for f in files:
        path = os.path.join(updates_dir, f)
        print(f"[UPDATE_SYSTEM] Uruchamiam aktualizację: {path}")
        try:
            parse_mpx_file(path)
        except SystemExit as e:
            print(f"[UPDATE_SYSTEM] Aktualizacja zakończyła się EXIT (kod: {e.code})")
        except Exception as e:
            print(f"[UPDATE_SYSTEM] Błąd podczas aktualizacji {f}: {e}")

    print("[UPDATE_SYSTEM] Wszystkie aktualizacje zostały wykonane.")


def register():
    register_command("RUN_UPDATES", handle_run_updates)
    print("[INFO][PLUGINS] Plugin UPDATE_SYSTEM zarejestrowany")
