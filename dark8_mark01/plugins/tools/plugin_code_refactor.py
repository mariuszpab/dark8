# plugin_code_refactor.py
from dark8_mark01.utils.dark8_llm import llm_generate


def handle_CODE_REFACTOR(task: dict, context: dict) -> dict:
    code = task.get("content")
    if not code:
        return {"error": "CODE_REFACTOR wymaga pola 'content' (kod źródłowy)"}

    prompt = f"Zrefaktoryzuj ten kod:\n\n{code}"
    result = llm_generate(prompt)

    return {
        "status": "ok",
        "refactored": result,
    }
