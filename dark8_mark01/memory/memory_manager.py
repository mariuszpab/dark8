# memory_manager.py
# DARK8 OS — Memory Layer: zarządzanie pamięcią

from dark8_mark01.memory.memory_store import load_memory, save_memory


def remember_project(path: str):
    mem = load_memory()
    projects = mem.get("projects", [])

    if path not in projects:
        projects.append(path)

    mem["projects"] = projects
    save_memory(mem)
    return f"Zapisano projekt w pamięci: {path}"


def remember_goal(goal: str):
    mem = load_memory()
    goals = mem.get("goals", [])
    goals.append(goal)
    mem["goals"] = goals
    save_memory(mem)
    return f"Zapisano cel: {goal}"


def remember_step(goal: str, step: dict):
    mem = load_memory()
    history = mem.get("history", {})
    if goal not in history:
        history[goal] = []
    history[goal].append(step)
    mem["history"] = history
    save_memory(mem)


def get_projects():
    mem = load_memory()
    return mem.get("projects", [])


def get_goals():
    mem = load_memory()
    return mem.get("goals", [])


def get_history(goal: str):
    mem = load_memory()
    return mem.get("history", {}).get(goal, [])
