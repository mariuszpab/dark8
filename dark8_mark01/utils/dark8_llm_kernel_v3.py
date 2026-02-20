import json
import requests
from typing import Optional, Literal

OLLAMA_HOST = "http://127.0.0.1:11434"

# Rejestr modeli, którymi kernel może zarządzać
LLMModelName = Literal["llama_main", "qwen_boost"]

LLM_MODELS: dict[LLMModelName, str] = {
    "llama_main": "llama3.2:1b",
    "qwen_boost": "qwen2.5:1.5b",
}


class LLMKernelError(Exception):
    """Błąd warstwy kernela LLM (do logów / auto-fix / watchdog)."""
    pass


def _ollama_generate_raw(model: str, prompt: str, system_prompt: Optional[str] = None, timeout: Optional[float] = 120.0) -> str:
    """
    Niski poziom: bezpośrednie wywołanie /api/generate.
    - timeout w sekundach (None = brak limitu, ale lepiej mieć twardy limit)
    """
    url = f"{OLLAMA_HOST}/api/generate"

    payload: dict = {
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
        raise LLMKernelError(f"[LLM TIMEOUT] Model '{model}' przekroczył limit czasu: {e}") from e
    except requests.exceptions.ConnectionError as e:
        raise LLMKernelError(f"[LLM CONNECTION] Brak połączenia z Ollama na {OLLAMA_HOST}: {e}") from e
    except Exception as e:
        raise LLMKernelError(f"[LLM ERROR] Wyjątek HTTP podczas komunikacji z Ollama: {e}") from e

    try:
        data = resp.json()
    except json.JSONDecodeError as e:
        raise LLMKernelError("[LLM ERROR] Nieprawidłowa odpowiedź JSON z Ollama.") from e

    return (data.get("response") or "").strip()


def llm_kernel_generate(
    prompt: str,
    system_prompt: Optional[str] = None,
    model_name: LLMModelName = "llama_main",
    allow_fallback: bool = True,
) -> str:
    """
    Główna funkcja kernela v3:
    - wybiera model po nazwie logicznej (llama_main / qwen_boost),
    - obsługuje błędy,
    - opcjonalnie robi fallback na inny model.
    """
    if model_name not in LLM_MODELS:
        raise LLMKernelError(f"[LLM CONFIG] Nieznany model logiczny: {model_name}")

    primary_model = LLM_MODELS[model_name]

    # 1. Próba z modelem głównym
    try:
        return _ollama_generate_raw(primary_model, prompt, system_prompt)
    except LLMKernelError as e_primary:
        # Jeśli fallback wyłączony → od razu błąd w górę
        if not allow_fallback:
            raise

        # 2. Fallback: jeśli prosiliśmy o qwen_boost → spróbuj llama_main
        #    jeśli prosiliśmy o llama_main → spróbuj qwen_boost
        fallback_model_name: Optional[LLMModelName] = None
        if model_name == "qwen_boost":
            fallback_model_name = "llama_main"
        elif model_name == "llama_main":
            fallback_model_name = "qwen_boost"

        if not fallback_model_name:
            # Teoretycznie nie powinno się zdarzyć, ale na wszelki wypadek:
            raise LLMKernelError(
                f"[LLM FALLBACK] Nie udało się użyć modelu '{primary_model}', brak fallbacku. Szczegóły: {e_primary}"
            ) from e_primary

        fallback_model = LLM_MODELS[fallback_model_name]

        try:
            return _ollama_generate_raw(fallback_model, prompt, system_prompt)
        except LLMKernelError as e_fallback:
            # Oba modele padły → zwracamy złożony błąd
            raise LLMKernelError(
                f"[LLM DOUBLE FAIL] Model główny '{primary_model}' i fallback '{fallback_model}' zawiodły.\n"
                f"Primary error: {e_primary}\nFallback error: {e_fallback}"
            ) from e_fallback
