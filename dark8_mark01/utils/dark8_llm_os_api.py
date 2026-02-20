from dark8_llm_kernel_v3 import llm_kernel_generate


def llm_system_task(prompt: str) -> str:
    """
    Zadania systemowe DARK8-OS:
    - zarządzanie agentem
    - operacje OS
    - logika sterowania
    - odpowiedzi stabilne i szybkie
    """
    return llm_kernel_generate(
        prompt=prompt,
        system_prompt="Jesteś modułem systemowym DARK8-OS. Odpowiadasz precyzyjnie, stabilnie i zwięźle.",
        model_name="llama_main",
        allow_fallback=True,
    )


def llm_analysis_task(prompt: str) -> str:
    """
    Zadania analityczne:
    - snapshot engine
    - analiza logów
    - wykrywanie błędów
    - diagnoza systemu
    """
    return llm_kernel_generate(
        prompt=prompt,
        system_prompt="Jesteś modułem analitycznym DARK8-OS. Analizujesz logi, błędy i stan systemu.",
        model_name="qwen_boost",
        allow_fallback=True,
    )


def llm_fix_task(prompt: str) -> str:
    """
    Zadania naprawcze:
    - auto-fix
    - generowanie poprawek
    - naprawa konfiguracji
    - korekta błędów
    """
    return llm_kernel_generate(
        prompt=prompt,
        system_prompt="Jesteś modułem AUTO-FIX DARK8-OS. Generujesz konkretne poprawki i rozwiązania.",
        model_name="qwen_boost",
        allow_fallback=True,
    )
