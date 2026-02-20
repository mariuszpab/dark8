from dark8_mark01.agent.agent_runner import run_agent_task
from dark8_mark01.agent.agent_plan import build_plan


def run_autonomic_task(task_description: str):
    """
    Uproszczony autonomiczny agent zoptymalizowany pod lokalne modele.
    Zwraca prostą strukturę: task + plan + wynik.
    """

    plan = build_plan(task_description)
    result = run_agent_task(task_description)

    return {
        "task": task_description,
        "plan": plan,
        "result": result
    }
