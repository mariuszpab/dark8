import os
import json
import re
from ..command_registry import register_command
from ..commands.patch_ops import load_json_lenient


# Globalna konfiguracja
_config = {}


# ---------------------------------------------------------
# Pomocnicze funkcje do pracy ze ścieżkami
# ---------------------------------------------------------

def _set_path(data, path, value):
    keys = path.split(".")
    d = data
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


def _get_path(data, path):
    keys = path.split(".")
    d = data
    for k in keys:
        if k not in d:
            return None
        d = d[k]
    return d


# ---------------------------------------------------------
# Komendy CONFIG
# ---------------------------------------------------------

def handle_config_load(command, args, block):
    path = args.strip()
    if not path:
        print("[ERROR][CONFIG] Brak ścieżki pliku.")
        return

    if not os.path.exists(path):
        print(f"[ERROR][CONFIG] Plik nie istnieje: {path}")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        data = load_json_lenient(text)
        if not isinstance(data, dict):
            print("[ERROR][CONFIG] Plik konfiguracyjny musi zawierać obiekt JSON.")
            return

        _config.clear()
        _config.update(data)

        print(f"[CONFIG] Załadowano konfigurację z: {path}")

    except Exception as e:
        print(f"[ERROR][CONFIG] Błąd ładowania: {e}")


def handle_config_save(command, args, block):
    path = args.strip()
    if not path:
        print("[ERROR][CONFIG] Brak ścieżki pliku.")
        return

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(_config, f, indent=2, ensure_ascii=False)
        print(f"[CONFIG] Zapisano konfigurację do: {path}")

    except Exception as e:
        print(f"[ERROR][CONFIG] Błąd zapisu: {e}")


def handle_config_set(command, args, block):
    parts = args.split(maxsplit=1)
    if len(parts) != 2:
        print("[ERROR][CONFIG] Użycie: CONFIG_SET <ścieżka> <wartość>")
        return

    path, value_raw = parts

    # Spróbuj sparsować wartość jako JSON
    try:
        value = load_json_lenient(value_raw)
    except:
        # Jeśli nie jest JSON-em, traktujemy jako string
        value = value_raw

    _set_path(_config, path, value)
    print(f"[CONFIG] Ustawiono {path} = {value}")


def handle_config_get(command, args, block):
    path = args.strip()
    if not path:
        print("[ERROR][CONFIG] Brak ścieżki.")
        return

    value = _get_path(_config, path)
    print(f"[CONFIG] {path} = {value}")


# ---------------------------------------------------------
# Rejestracja pluginu
# ---------------------------------------------------------

def register():
    register_command("CONFIG_LOAD", handle_config_load)
    register_command("CONFIG_SAVE", handle_config_save)
    register_command("CONFIG_SET", handle_config_set)
    register_command("CONFIG_GET", handle_config_get)

    print("[INFO][PLUGINS] Plugin CONFIG zarejestrowany")
