import os

from dark8_llm_os_api import llm_fix_task

MAX_FILE_CHARS = 8000
MAX_FILES = 80


def _collect_python_files(root_dir):
    py_files = []
    for current_root, dirs, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(current_root, f))
    return sorted(py_files)


def _read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception as e:
            return f"# [DARK8] Nie udało się odczytać pliku {path}: {e}"
    except Exception as e:
        return f"# [DARK8] Nie udało się odczytać pliku {path}: {e}"


def _write_file_safe(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _build_auto_fix_prompt(rel_path, original_code):
    if len(original_code) > MAX_FILE_CHARS:
        original_code = (
            original_code[:MAX_FILE_CHARS]
            + f"\n\n# [DARK8] Plik przycięty do {MAX_FILE_CHARS} znaków.\n"
        )

    return f"""
Jesteś modułem AUTO-FIX DARK8-OS.

Otrzymasz pełną treść pojedynczego pliku Pythona z projektu DARK8.

Plik: {rel_path}

Twoje zadanie:
1. Popraw błędy (logiczne, strukturalne, importy, brakujące elementy).
2. Uprość i uporządkuj kod.
3. Zachowaj pełną funkcjonalność pliku.
4. Zwróć WYŁĄCZNIE kompletną treść poprawionego pliku .py.

Oryginalny kod:
{original_code}
"""


def auto_fix_dark8_project(root_dir, output_root):
    """
    Auto-Fix Engine v3:
    - przetwarza plik po pliku
    - każdy plik ma osobny prompt
    - używa OS API → llm_fix_task()
    """

    py_files = _collect_python_files(root_dir)
    if len(py_files) > MAX_FILES:
        py_files = py_files[:MAX_FILES]

    summary = []
    summary.append(f"[DARK8 AUTO-FIX v3] Start auto-fix: {root_dir}")
    summary.append(f"[DARK8 AUTO-FIX v3] Katalog wyjściowy: {output_root}")
    summary.append(f"[DARK8 AUTO-FIX v3] Liczba plików: {len(py_files)}\n")

    for idx, path in enumerate(py_files, start=1):
        rel_path = os.path.relpath(path, root_dir)
        original_code = _read_file_safe(path)

        summary.append(f"[{idx}/{len(py_files)}] Przetwarzanie: {rel_path}")

        prompt = _build_auto_fix_prompt(rel_path, original_code)
        fixed_code = llm_fix_task(prompt)

        target_path = os.path.join(output_root, rel_path)
        _write_file_safe(target_path, fixed_code)

        summary.append(f"Zapisano poprawioną wersję: {target_path}\n")

    summary.append("[DARK8 AUTO-FIX v3] Zakończono auto-fix projektu.")
    return "\n".join(summary)
