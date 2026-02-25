import requests

# ---------------------------------------------------------
# DARK8‑OS API — Kernel v3
# Centralny moduł komunikacji z backendem LLM (Ollama)
# ---------------------------------------------------------

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
TIMEOUT = 120


def _call_ollama(model: str, prompt: str) -> str:
    """
    Niskopoziomowe wywołanie backendu LLM.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except Exception as e:
        return f"[OS-API ERROR] {e}"


# ---------------------------------------------------------
# 1. ANALIZA KODU
# ---------------------------------------------------------

def llm_analysis_task(prompt: str) -> str:
    """
    Analiza kodu — model techniczny.
    """
    return _call_ollama("codellama:13b", prompt)


# ---------------------------------------------------------
# 2. AUTO-FIX KODU
# ---------------------------------------------------------

def llm_fix_task(prompt: str) -> str:
    """
    Auto‑fix kodu — model techniczny.
    """
    return _call_ollama("codellama:13b", prompt)


# ---------------------------------------------------------
# 3. PLANOWANIE ZADAŃ (AGENT)
# ---------------------------------------------------------

def llm_plan_task(prompt: str) -> str:
    """
    Tworzenie planu działania — model reasoning.
    """
    return _call_ollama("llama3:8b", prompt)


# ---------------------------------------------------------
# 4. WYKONANIE ZADAŃ (AGENT)
# ---------------------------------------------------------

def llm_execute_task(prompt: str) -> str:
    """
    Wykonanie kroków planu — model wykonawczy.
    """
    return _call_ollama("llama3:8b", prompt)
