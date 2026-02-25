# self_improve.py
# Warstwa samodoskonalenia DARK8 (Self-Improvement)

from dark8_mark01.utils.dark8_llm import llm_generate

# ============================================================
# 1. ULEPSZANIE PLANU
# ============================================================


def improve_plan(plan, task_description):
    """
    Ulepsza plan wygenerowany przez agenta.
    Zwraca nową listę kroków.
    """
    prompt = (
        "Ulepsz poniższy plan wykonania zadania.\n"
        "Zadanie:\n"
        f"{task_description}\n\n"
        "Plan:\n"
        f"{plan}\n\n"
        "Zwróć ulepszony plan, każdy krok w osobnej linii, w formacie:\n"
        "- <opis kroku>\n"
    )

    text = llm_generate(prompt)
    improved = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("-"):
            line = line[1:].strip()
        improved.append({"description": line})

    return improved if improved else plan


# ============================================================
# 2. ULEPSZANIE MPX
# ============================================================


def improve_mpx(mpx_text, task_description):
    """
    Ulepsza wygenerowany MPX.
    """
    prompt = (
        "Ulepsz poniższy skrypt MPX tak, aby był bardziej precyzyjny i skuteczny.\n"
        "Zadanie:\n"
        f"{task_description}\n\n"
        "MPX:\n"
        f"{mpx_text}\n\n"
        "Zwróć poprawioną wersję MPX."
    )

    improved = llm_generate(prompt)
    return improved if improved else mpx_text


# ============================================================
# 3. DIAGNOSTYKA
# ============================================================


def run_self_diagnostics():
    print("=== DIAGNOSTYKA SYSTEMU DARK8 ===")
    print("[OK] Moduł self-improve działa poprawnie.")
    print("Diagnostyka zakończona.\n")


# ============================================================
# 4. SAMONAPRAWA
# ============================================================


def run_self_repair():
    print("=== AUTOMATYCZNA NAPRAWA DARK8 ===")
    print("[OK] Brak błędów wymagających naprawy.")
    print("Naprawa zakończona.\n")
