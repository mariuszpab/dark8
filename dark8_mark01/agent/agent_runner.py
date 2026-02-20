from dark8_llm_os_api import llm_execute_task


def run_agent_task(step_description: str) -> str:
    """
    Wykonuje pojedynczy krok planu agenta.
    Kernel v3 używa llm_execute_task() zamiast llm_system_task().
    """

    prompt = f"""
Jesteś modułem wykonawczym DARK8‑OS.

Otrzymasz opis pojedynczego kroku planu.

Wykonaj ten krok i zwróć wynik w formie tekstowej.

Krok:
{step_description}
"""

    result = llm_execute_task(prompt)
    return result
