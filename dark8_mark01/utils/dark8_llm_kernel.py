import json
import requests
from typing import Optional, Literal

# Adres backendu Ollama
OLLAMA_HOST = "http://127.0.0.1:11434"

# Logiczne nazwy modeli — system sam wybiera fizyczny model
LLMModelName = Literal["llama_main", "qwen_boost"]

LLM_MODELS: dict[LLMModelName, str] = {
    "llama_main": "llama3.2:1b",       # stabilny, szybki, idealny do kernela
    "qwen_boost": "qwen2.5:1.5b",      # mocniejszy, do analizy i auto-fix
}


class LLMKernelError(Exception):
    """Błąd warstwy kernela LLM."""
    pass


def _ollama_generate_raw(
    model: str,
    prompt: str,
    system_prompt: Optional[str] = None,
    timeout: float = 120.0
) -> str:
    """
    Niski poziom: bezpośrednie wywołanie /api/generate.
    - timeout = 120s (twardy limit)
    - stream = False
    """
    url = f"{OLLAMA_HOST}/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    if system_prompt:
        payload["system"] = system_prompt

    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.Timeout as e:
        raise LLMKernelError(f"[LLM TIMEOUT] Model '{model}' przekroczył limit czasu.") from e
    except requests.exceptions.ConnectionError as e:
        raise LLMKernelError(f"[LLM CONNECTION] Brak połączenia z Ollama: {e}") from e
    except Exception as e:
        raise LLMKernelError(f"[LLM ERROR] Wyjątek HTTP: {e}") from e

    try:
        data = resp.json()
    except json.JSONDecodeError as e:
        raise LLMKernelError("[LLM ERROR] Nieprawidłowa odpowiedź JSON.") from e

    return (data.get("response") or "").strip()


def llm_kernel_generate(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_name: LLMModelName = "llama_main",
    allow_fallback: bool = True,
) -> str:
    """
    Główna funkcja kernela DARK8-OS v3:
    - wybiera model logiczny,
    - obsługuje błędy,
    - robi automatyczny fallback,
    - zwraca czystą odpowiedź LLM.
    """

    if model_name not in LLM_MODELS:
        raise LLMKernelError(f"[LLM CONFIG] Nieznany model logiczny: {model_name}")

    primary_model = LLM_MODELS[model_name]

    # 1. Próba z modelem głównym
    try:
        return _ollama_generate_raw(primary_model, prompt, system_prompt)
    except LLMKernelError as e_primary:
        if not allow_fallback:
            raise

        # 2. Automatyczny fallback
        fallback_name = "qwen_boost" if model_name == "llama_main" else "llama_main"
        fallback_model = LLM_MODELS[fallback_name]

        try:
            return _ollama_generate_raw(fallback_model, prompt, system_prompt)
        except LLMKernelError as e_fallback:
            raise LLMKernelError(
                f"[LLM DOUBLE FAIL] Model główny '{primary_model}' i fallback '{fallback_model}' zawiodły.\n"
                f"Primary: {e_primary}\nFallback: {e_fallback}"
            ) from e_fallback
