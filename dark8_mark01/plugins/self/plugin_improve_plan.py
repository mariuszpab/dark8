# plugin_improve_plan.py
from dark8_mark01.agent.self_improve import improve_plan

def handle_IMPROVE_PLAN(task, context):
    task_description = task.get("task_description")
    plan = task.get("plan")

    if not task_description:
        return {"error": "IMPROVE_PLAN wymaga 'task_description'"}
    if not isinstance(plan, list):
        return {"error": "IMPROVE_PLAN wymaga 'plan' jako listy kroków"}

    new_plan = improve_plan(task_description, plan)
    return {
        "status": "ok",
        "plan": new_plan,
    }
