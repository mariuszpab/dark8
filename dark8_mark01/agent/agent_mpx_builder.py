# agent_mpx_builder.py
# Budowanie prostego scenariusza .mpx z planu

def build_mpx_from_plan(plan: list[dict], task_description: str) -> str:
    """
    Z listy kroków buduje prosty scenariusz .mpx.
    Na razie: szablon + komentarze.
    """
    lines = []
    lines.append("# AUTO-GENERATED MPX SCENARIO")
    lines.append(f"# TASK: {task_description}")
    lines.append("")

    for i, step in enumerate(plan, start=1):
        desc = step.get("description", f"Krok {i}")
        lines.append(f"# KROK {i}: {desc}")
        lines.append("# TODO: dopasuj odpowiednie komendy")
        lines.append("")
        # Na tym etapie zostawiamy miejsce na ręczne lub LLM-owe uzupełnienie

    return "\n".join(lines)
