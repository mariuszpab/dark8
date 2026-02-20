from dark8_llm_os_api import llm_plan_task


def build_plan(task_description: str) -> str:
    """
    Tworzy plan działania dla agenta.
    Kernel v3 używa llm_plan_task() zamiast llm_system_task().
    """

    prompt = f"""
Jesteś modułem planowania DARK8‑OS.

Twoim zadaniem jest stworzenie jasnego, krokowego planu wykonania zadania.

Zadanie użytkownika:
{task_description}

Zwróć plan w formie listy kroków.
"""

    result = llm_plan_task(prompt)
    return result
