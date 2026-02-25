import os
import shutil

from ..command_registry import register_command


def log_info(msg):
    print(f"[INFO][FILE_OPS] {msg}")


def log_error(msg):
    print(f"[ERROR][FILE_OPS] {msg}")


# ---------------------------------------------------------
# GŁÓWNY HANDLER
# ---------------------------------------------------------


def handle(command, args, block):
    """
    Główny router komend plikowych.
    Każda komenda trafia tutaj, bo rejestrujemy je wszystkie
    jako aliasy do tej jednej funkcji.
    """

    if command == "WRITE_FILE":
        return write_file(args, block)

    if command == "APPEND_FILE":
        return append_file(args, block)

    if command == "READ_FILE":
        return read_file(args)

    if command == "DELETE_FILE":
        return delete_file(args)

    if command == "COPY_FILE":
        return copy_file(args)

    if command == "MOVE_FILE":
        return move_file(args)

    if command == "MAKE_DIR":
        return make_dir(args)

    if command == "DELETE_DIR":
        return delete_dir(args)

    if command == "LIST_DIR":
        return list_dir(args)

    log_error(f"Nieznana komenda FILE_OPS: {command}")


# ---------------------------------------------------------
# IMPLEMENTACJE KOMEND
# ---------------------------------------------------------


def write_file(path, block):
    path = path.strip()
    if not path:
        log_error("WRITE_FILE: brak ścieżki.")
        return

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(block if block else "")
        log_info(f"Zapisano plik: {path}")
    except Exception as e:
        log_error(f"WRITE_FILE błąd: {e}")


def append_file(path, block):
    path = path.strip()
    if not path:
        log_error("APPEND_FILE: brak ścieżki.")
        return

    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(block if block else "")
        log_info(f"Dopisano do pliku: {path}")
    except Exception as e:
        log_error(f"APPEND_FILE błąd: {e}")


def read_file(path):
    path = path.strip()
    if not path:
        log_error("READ_FILE: brak ścieżki.")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        log_info(f"Zawartość pliku {path}:")
        print(content)
    except Exception as e:
        log_error(f"READ_FILE błąd: {e}")


def delete_file(path):
    path = path.strip()
    if not path:
        log_error("DELETE_FILE: brak ścieżki.")
        return

    try:
        os.remove(path)
        log_info(f"Usunięto plik: {path}")
    except FileNotFoundError:
        log_error(f"Plik nie istnieje: {path}")
    except Exception as e:
        log_error(f"DELETE_FILE błąd: {e}")


def copy_file(args):
    parts = args.split()
    if len(parts) != 2:
        log_error("COPY_FILE wymaga: COPY_FILE źródło cel")
        return

    src, dst = parts
    try:
        shutil.copy2(src, dst)
        log_info(f"Skopiowano {src} → {dst}")
    except Exception as e:
        log_error(f"COPY_FILE błąd: {e}")


def move_file(args):
    parts = args.split()
    if len(parts) != 2:
        log_error("MOVE_FILE wymaga: MOVE_FILE źródło cel")
        return

    src, dst = parts
    try:
        shutil.move(src, dst)
        log_info(f"Przeniesiono {src} → {dst}")
    except Exception as e:
        log_error(f"MOVE_FILE błąd: {e}")


def make_dir(path):
    path = path.strip()
    if not path:
        log_error("MAKE_DIR: brak ścieżki.")
        return

    try:
        os.makedirs(path, exist_ok=True)
        log_info(f"Utworzono katalog: {path}")
    except Exception as e:
        log_error(f"MAKE_DIR błąd: {e}")


def delete_dir(path):
    path = path.strip()
    if not path:
        log_error("DELETE_DIR: brak ścieżki.")
        return

    try:
        shutil.rmtree(path)
        log_info(f"Usunięto katalog: {path}")
    except FileNotFoundError:
        log_error(f"Katalog nie istnieje: {path}")
    except Exception as e:
        log_error(f"DELETE_DIR błąd: {e}")


def list_dir(path):
    path = path.strip()
    if not path:
        log_error("LIST_DIR: brak ścieżki.")
        return

    try:
        items = os.listdir(path)
        log_info(f"Zawartość katalogu {path}:")
        for item in items:
            print(" -", item)
    except Exception as e:
        log_error(f"LIST_DIR błąd: {e}")


# ---------------------------------------------------------
# REJESTRACJA KOMEND W SYSTEMIE
# ---------------------------------------------------------


def register():
    """
    Rejestruje wszystkie komendy FILE_OPS w globalnym rejestrze.
    """
    for cmd in [
        "WRITE_FILE",
        "APPEND_FILE",
        "READ_FILE",
        "DELETE_FILE",
        "COPY_FILE",
        "MOVE_FILE",
        "MAKE_DIR",
        "DELETE_DIR",
        "LIST_DIR",
    ]:
        register_command(cmd, handle)
