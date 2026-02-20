import json
import requests

OLLAMA_HOST = "http://127.0.0.1:11434"
OLLAMA_MODEL = "llama3.2:3b"  # lub "deepseek-r1:1.5b"


def llm_kernel_generate(prompt: str, system_prompt: str | None = None) -> str:
    """
    Kernel LLM DARK8-OS
    - timeout = None (brak limitu)
    - stream = False (pełna odpowiedź)
    """

    url = f"{OLLAMA_HOST}/api/generate"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    if system_prompt:
        payload["system"] = system_prompt

    try:
        # timeout=None = brak limitu
        resp = requests.post(url, json=payload, timeout=None)
        resp.raise_for_status()
    except Exception as e:
        return f"[LLM ERROR] Wyjątek podczas komunikacji z Ollama: {e}"

    try:
        data = resp.json()
    except json.JSONDecodeError:
        return "[LLM ERROR] Nieprawidłowa odpowiedź JSON z Ollama."

    return data.get("response", "").strip()
