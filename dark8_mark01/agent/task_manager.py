# C:\DARK8_MARK01\dark8_mark01\agent\task_manager.py

from dark8_mark01.core.dispatcher import dispatch

def execute_plan(steps: list[dict]) -> list[dict]:
    """
    Wykonuje kolejne kroki planu.
    Zwraca listę wyników: [{"step": ..., "result": "..."}]
    """
    results = []

    for i, step in enumerate(steps, start=1):
        intent = step["intent"]
        args = step.get("args", {})
        desc = step.get("description", "")

        result = dispatch(intent, args)

        results.append({
            "index": i,
            "intent": intent,
            "description": desc,
            "args": args,
            "result": result,
        })

    return results
