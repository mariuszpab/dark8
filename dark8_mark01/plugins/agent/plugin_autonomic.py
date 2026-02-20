# plugin_autonomic.py
from dark8_mark01.agent.autonomic_agent import run_autonomic_task

def handle_AUTONOMIC_TASK(task, context):
    description = task.get("task_description")
    max_iters = task.get("max_iters", 3)
    target_score = task.get("target_score", 0.8)

    if not description:
        return {"error": "AUTONOMIC_TASK wymaga 'task_description'"}

    result = run_autonomic_task(description,
                                max_iters=max_iters,
                                target_score=target_score)

    return {
        "status": "ok",
        "result": result,
    }
