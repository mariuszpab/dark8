import os
from dark8_llm_os_api import llm_analysis_task

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


def analyze_dark8_project(root_dir):
    """
    Snapshot Engine v3:
    - analiza plik po pliku
    - każdy plik ma osobny prompt
    - używa OS API → llm_analysis_task()
    """

    py_files = _collect_python_files(root_dir)
    if len(py_files) > MAX_FILES:
        py_files = py_files[:MAX_FILES]

    report_parts = []
    report_parts.append(
        f"[DARK8] Analiza projektu – znaleziono {len(py_files)} plików (limit {MAX_FILES}).\n"
    )

    for idx, path in enumerate(py_files, start=1):
        rel_path = os.path.relpath(path, root_dir)
        code = _read_file_safe(path)

        if len(code) > MAX_FILE_CHARS:
            code = code[:MAX_FILE_CHARS] + f"\n\n# [DARK8] Plik przycięty do {MAX_FILE_CHARS} znaków.\n"

        prompt = f"""
Jesteś modułem analitycznym DARK8-OS.

Otrzymasz pojedynczy plik Pythona z projektu DARK8.

Plik: {rel_path}

Twoje zadanie:
1. Wskaż potencjalne błędy (logiczne, strukturalne, importy, brakujące elementy).
2. Wskaż miejsca mogące powodować wyjątki.
3. Zaproponuj konkretne poprawki (z fragmentami kodu).
4. Zaproponuj uproszczenia i refaktoryzację.

Kod pliku:
{code}
"""

        result = llm_analysis_task(prompt)

        block = (
            "============================================\n"
            f"ANALIZA PLIKU: {rel_path} ({idx}/{len(py_files)})\n"
            "============================================\n"
            f"{result}\n\n"
        )
        report_parts.append(block)

    return "\n".join(report_parts)
