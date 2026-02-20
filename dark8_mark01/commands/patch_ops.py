import os
import json
import yaml
import re
from ..command_registry import register_command


def log_info(msg):
    print(f"[INFO][PATCH] {msg}")


def log_error(msg):
    print(f"[ERROR][PATCH] {msg}")


# ---------------------------------------------------------
# GŁÓWNY HANDLER
# ---------------------------------------------------------

def handle(command, args, block):
    if command == "PATCH_FILE":
        return patch_file(args, block)

    if command == "PATCH_DIFF":
        return patch_diff(args, block)

    log_error(f"Nieznana komenda PATCH_OPS: {command}")


# ---------------------------------------------------------
# JSON5 / JSONC — parser tolerujący komentarze i trailing commas
# ---------------------------------------------------------

def load_json_lenient(text):
    """
    Próbuje najpierw zwykły JSON.
    Jeśli się wywali → usuwa komentarze, trailing commas i próbuje ponownie.
    """

    # 1) Najpierw spróbuj czysty JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2) Usuń komentarze // i /* ... */
    def strip_comments(s):
        s = re.sub(r"/\*.*?\*/", "", s, flags=re.DOTALL)
        s = re.sub(r"//.*?$", "", s, flags=re.MULTILINE)
        return s

    # 3) Usuń trailing commas
    def strip_trailing_commas(s):
        s = re.sub(r",\s*([}\]])", r"\1", s)
        return s

    cleaned = strip_comments(text)
    cleaned = strip_trailing_commas(cleaned)

    # 4) Spróbuj ponownie
    try:
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(f"Nie można sparsować JSON/JSON5: {e}") from e


# ---------------------------------------------------------
# PATCH_FILE — JSON/YAML z listą operacji
# ---------------------------------------------------------

def patch_file(path, patch_text):
    path = path.strip()
    if not path:
        log_error("PATCH_FILE: brak ścieżki.")
        return

    if not os.path.exists(path):
        log_error(f"Plik nie istnieje: {path}")
        return

    # Wczytaj oryginał
    try:
        with open(path, "r", encoding="utf-8") as f:
            original_text = f.read()
    except Exception as e:
        log_error(f"Nie można odczytać pliku: {e}")
        return

    # JSON czy YAML?
    is_yaml = path.endswith(".yaml") or path.endswith(".yml")

    try:
        if is_yaml:
            data = yaml.safe_load(original_text)
        else:
            data = load_json_lenient(original_text)
    except Exception as e:
        log_error(f"Nie można sparsować pliku: {e}")
        return

    # Wczytaj patch
    try:
        patch = load_json_lenient(patch_text)
    except Exception as e:
        log_error(f"Patch nie jest poprawnym JSON/JSON5: {e}")
        return

    if not isinstance(patch, dict) or "ops" not in patch:
        log_error("PATCH_FILE: brak listy 'ops'.")
        return

    # Wykonaj operacje
    for op in patch["ops"]:
        apply_operation(data, op)

    # Zapisz wynik
    try:
        with open(path, "w", encoding="utf-8") as f:
            if is_yaml:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            else:
                json.dump(data, f, indent=2, ensure_ascii=False)

        log_info(f"Zastosowano patch do pliku: {path}")

    except Exception as e:
        log_error(f"Błąd zapisu: {e}")


# ---------------------------------------------------------
# OPERACJE PATCHA
# ---------------------------------------------------------

def apply_operation(data, op):
    operation = op.get("op")
    path = op.get("path")

    if not operation or not path:
        log_error(f"Niepoprawna operacja: {op}")
        return

    keys = path.split(".")

    if operation == "set":
        value = op.get("value")
        set_value(data, keys, value)
        log_info(f"SET {path} = {value}")
        return

    if operation == "remove":
        remove_value(data, keys)
        log_info(f"REMOVE {path}")
        return

    if operation == "merge":
        value = op.get("value")
        merge_value(data, keys, value)
        log_info(f"MERGE {path}")
        return

    log_error(f"Nieznana operacja: {operation}")


def set_value(data, keys, value):
    d = data
    for k in keys[:-1]:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


def remove_value(data, keys):
    d = data
    for k in keys[:-1]:
        if k not in d:
            return
        d = d[k]
    d.pop(keys[-1], None)


def merge_value(data, keys, value):
    d = data
    for k in keys:
        if k not in d or not isinstance(d[k], dict):
            d[k] = {}
        d = d[k]

    if isinstance(value, dict):
        d.update(value)


# ---------------------------------------------------------
# PATCH_DIFF — pełny parser unified diff
# ---------------------------------------------------------

def patch_diff(path, diff_text):
    path = path.strip()
    if not path:
        log_error("PATCH_DIFF: brak ścieżki.")
        return

    if not os.path.exists(path):
        log_error(f"Plik nie istnieje: {path}")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            original_lines = f.readlines()
    except Exception as e:
        log_error(f"Nie można odczytać pliku: {e}")
        return

    try:
        patched_lines = apply_unified_diff(
            original_lines,
            diff_text.splitlines(keepends=False)
        )
    except Exception as e:
        log_error(f"Nie można zastosować diff: {e}")
        return

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(patched_lines)
        log_info(f"Zastosowano diff do pliku: {path}")
    except Exception as e:
        log_error(f"Błąd zapisu: {e}")


def apply_unified_diff(original_lines, diff_lines):
    """
    Minimalny parser unified diff:
    - ignoruje linie --- / +++
    - obsługuje hunki @@ ... @@
    - ' ' = linia kontekstowa
    - '-' = usuń linię z oryginału
    - '+' = dodaj linię do wyniku
    """

    result = []
    orig_index = 0
    i = 0
    n = len(diff_lines)

    while i < n:
        line = diff_lines[i]

        if line.startswith('---') or line.startswith('+++'):
            i += 1
            continue

        if line.startswith('@@'):
            i += 1
            while i < n and not diff_lines[i].startswith('@@') and not diff_lines[i].startswith('---') and not diff_lines[i].startswith('+++'):
                hline = diff_lines[i]
                if not hline:
                    i += 1
                    continue

                prefix = hline[0]
                content = hline[1:] + "\n"

                if prefix == ' ':
                    if orig_index < len(original_lines):
                        result.append(original_lines[orig_index])
                        orig_index += 1
                    else:
                        result.append(content)

                elif prefix == '-':
                    if orig_index < len(original_lines):
                        orig_index += 1

                elif prefix == '+':
                    result.append(content)

                else:
                    result.append(hline + "\n")

                i += 1
        else:
            i += 1

    while orig_index < len(original_lines):
        result.append(original_lines[orig_index])
        orig_index += 1

    return result


# ---------------------------------------------------------
# REJESTRACJA KOMEND
# ---------------------------------------------------------

def register():
    for cmd in ["PATCH_FILE", "PATCH_DIFF"]:
        register_command(cmd, handle)
