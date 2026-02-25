# plugin_code_generate.py
from dark8_mark01.utils.dark8_llm import llm_generate


def handle_CODE_GENERATE(task: dict, context: dict) -> dict:
    prompt = task.get("prompt")
    if not prompt:
        return {"error": "CODE_GENERATE wymaga pola 'prompt'"}

    code = llm_generate(prompt)

    return {
        "status": "ok",
        "prompt": prompt,
        "code": code,
    }
