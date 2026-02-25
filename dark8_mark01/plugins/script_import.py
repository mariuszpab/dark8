import os

from ..command_registry import register_command
from ..mpx_parser import parse_mpx_file

# Zestaw ścieżek już zaimportowanych, aby uniknąć pętli
_imported_scripts = set()


def handle_import(command, args, block):
    """
    IMPORT <ścieżka>
    Wykonuje inny plik MPX.
    """
    path = args.strip()

    if not path:
        print("[ERROR][IMPORT] Brak ścieżki do pliku.")
        return

    if not os.path.exists(path):
        print(f"[ERROR][IMPORT] Plik nie istnieje: {path}")
        return

    # Normalizacja ścieżki
    norm = os.path.normpath(path)

    # Zapobieganie zapętleniom
    if norm in _imported_scripts:
        print(f"[IMPORT] Pomijam (już zaimportowano): {norm}")
        return

    print(f"[IMPORT] Importuję skrypt: {norm}")
    _imported_scripts.add(norm)

    try:
        parse_mpx_file(norm)
    except SystemExit as e:
        print(f"[IMPORT] Skrypt zakończył się EXIT (kod: {e.code})")
    except Exception as e:
        print(f"[ERROR][IMPORT] Błąd podczas importu {norm}: {e}")


def register():
    register_command("IMPORT", handle_import)
    print("[INFO][PLUGINS] Plugin SCRIPT_IMPORT zarejestrowany")
