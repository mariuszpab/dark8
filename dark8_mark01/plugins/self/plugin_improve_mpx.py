# plugin_improve_mpx.py
from dark8_mark01.agent.self_improve import improve_mpx


def handle_IMPROVE_MPX(task, context):
    task_description = task.get("task_description")
    mpx_text = task.get("mpx")

    if not task_description:
        return {"error": "IMPROVE_MPX wymaga 'task_description'"}
    if not isinstance(mpx_text, str):
        return {"error": "IMPROVE_MPX wymaga 'mpx' jako string"}

    new_mpx = improve_mpx(task_description, mpx_text)
    return {
        "status": "ok",
        "mpx": new_mpx,
    }
