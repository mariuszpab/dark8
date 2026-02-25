# agent_core.py
# DARK8 OS — AGENT LAYER (cele, planowanie, pamięć, shell, joby, meta-agent)

from dark8_mark01.agent.planner import plan_from_goal
from dark8_mark01.agent.task_manager import execute_plan

from dark8_mark01.memory.memory_manager import (
    remember_goal,
    remember_project,
    remember_step,
    get_projects,
    get_goals,
    get_history,
)

from dark8_mark01.core.dispatcher import dispatch

from dark8_mark01.jobs.job_manager import (
    create_job,
    start_job,
    finish_job,
    fail_job,
    list_jobs,
    get_job,
    kill_job,
)

from dark8_mark01.meta.meta_agent import (
    meta_analyze,
    meta_refactor,
    meta_extend,
    meta_create,
)


def handle_shell_like(text: str):
    stripped = text.strip()

    if stripped.startswith("dir") or stripped.startswith("ls"):
        parts = stripped.split()
        path = parts[1] if len(parts) > 1 else "."
        return "LIST_DIR", dispatch("LIST_DIR", {"path": path})

    if stripped.startswith("cd "):
        path = stripped.split(" ", 1)[1]
        return "CHANGE_DIR", dispatch("CHANGE_DIR", {"path": path})

    if stripped.startswith("python "):
        path = stripped.split(" ", 1)[1]
        return "RUN_PYTHON_SCRIPT", dispatch("RUN_PYTHON_SCRIPT", {"path": path})

    if stripped in ["pwd"]:
        return "SHOW_CWD", dispatch("SHOW_CWD", {})

    if stripped.startswith("mkdir "):
        path = stripped.split(" ", 1)[1]
        return "MAKE_DIR", dispatch("MAKE_DIR", {"path": path})

    if stripped.startswith("rmdir "):
        path = stripped.split(" ", 1)[1]
        return "REMOVE_DIR", dispatch("REMOVE_DIR", {"path": path})

    if stripped.startswith("rm ") or stripped.startswith("del "):
        path = stripped.split(" ", 1)[1]
        return "DELETE_FILE", dispatch("DELETE_FILE", {"path": path})

    if stripped.startswith("cp "):
        parts = stripped.split()
        if len(parts) >= 3:
            return "COPY_FILE", dispatch("COPY_FILE", {"src": parts[1], "dst": parts[2]})

    if stripped.startswith("mv "):
        parts = stripped.split()
        if len(parts) >= 3:
            return "MOVE_FILE", dispatch("MOVE_FILE", {"src": parts[1], "dst": parts[2]})

    if stripped.startswith("touch "):
        path = stripped.split(" ", 1)[1]
        return "TOUCH_FILE", dispatch("TOUCH_FILE", {"path": path})

    if stripped.startswith("cat ") or stripped.startswith("type "):
        path = stripped.split(" ", 1)[1]
        return "READ_FILE", dispatch("READ_FILE", {"path": path})

    return None


def interactive_memory_commands(text: str):
    t = text.lower()

    if "jakie projekty" in t:
        return "MEMORY_PROJECTS", "\n".join(get_projects())

    if "jakie cele" in t:
        return "MEMORY_GOALS", "\n".join(get_goals())

    if "pokaż historię celu" in t:
        goal = text.split("pokaż historię celu", 1)[1].strip()
        hist = get_history(goal)
        if not hist:
            return "MEMORY_HISTORY", "Brak historii dla tego celu."
        out = []
        for h in hist:
            out.append(f"Krok {h['index']}: {h['intent']} -> {h['result']}")
        return "MEMORY_HISTORY", "\n".join(out)

    return None


def interactive_jobs_commands(text: str):
    stripped = text.strip()

    if stripped == "jobs":
        jobs = list_jobs()
        if not jobs:
            return "JOBS_LIST", "Brak aktywnych jobów."
        lines = []
        for j in jobs:
            lines.append(
                f"[{j['id']}] {j['status']} | {j['goal']} | created: {j['created_at']}"
            )
        return "JOBS_LIST", "\n".join(lines)

    if stripped.startswith("job "):
        try:
            job_id = int(stripped.split()[1])
        except (ValueError, IndexError):
            return "JOB_DETAIL", "Niepoprawne ID joba."
        job = get_job(job_id)
        if not job:
            return "JOB_DETAIL", f"Brak joba o ID: {job_id}"
        lines = [
            f"ID: {job['id']}",
            f"Goal: {job['goal']}",
            f"Status: {job['status']}",
            f"Created: {job['created_at']}",
            f"Started: {job['started_at']}",
            f"Finished: {job['finished_at']}",
            f"Result: {job['result']}",
        ]
        return "JOB_DETAIL", "\n".join(lines)

    if stripped.startswith("kill "):
        try:
            job_id = int(stripped.split()[1])
        except (ValueError, IndexError):
            return "JOB_KILL", "Niepoprawne ID joba."
        msg = kill_job(job_id)
        return "JOB_KILL", msg

    return None


def mode_meta():
    print("\n[TRYB META-AGENTA] 'analyze <plik>', 'refactor <plik> :: instrukcja',")
    print("                   'extend <plik> :: instrukcja', 'create <plik> :: instrukcja'.")
    print("                   'exit' aby wrócić.\n")
    while True:
        text = input("META > ").strip()
        if text.lower() in ["exit", "quit"]:
            break

        if text.startswith("analyze "):
            path = text.split(" ", 1)[1].strip()
            print(meta_analyze(path))
            continue

        if text.startswith("refactor "):
            parts = text.split("::")
            if len(parts) < 2:
                print("Użycie: refactor <plik> :: instrukcja")
                continue
            path = parts[0].split()[1].strip()
            instruction = parts[1].strip()
            print(meta_refactor(path, instruction))
            continue

        if text.startswith("extend "):
            parts = text.split("::")
            if len(parts) < 2:
                print("Użycie: extend <plik> :: instrukcja")
                continue
            path = parts[0].split()[1].strip()
            instruction = parts[1].strip()
            print(meta_extend(path, instruction))
            continue

        if text.startswith("create "):
            parts = text.split("::")
            if len(parts) < 2:
                print("Użycie: create <plik> :: instrukcja")
                continue
            path = parts[0].split()[1].strip()
            instruction = parts[1].strip()
            print(meta_create(path, instruction))
            continue

        print("Nieznana komenda meta-agenta.")


def run_agent(goal: str):
    print(f"[AGENT] Cel: {goal}")

    remember_goal(goal)

    plan = plan_from_goal(goal)
    print(f"[AGENT] Plan zawiera {len(plan)} kroków.")

    results = execute_plan(plan)

    for r in results:
        remember_step(goal, r)

    for step in plan:
        if step["intent"] == "CREATE_PROJECT":
            remember_project(step["args"]["path"])

    print("[AGENT] Wyniki wykonania:")
    for r in results:
        print(f"  Krok {r['index']}: {r['intent']} -> {r['result']}")

    return results


def run_agent_as_job(goal: str):
    job_id = create_job(goal)
    print(f"[JOB] Utworzono job {job_id} dla celu: {goal}")
    try:
        start_job(job_id)
        result = run_agent(goal)
        finish_job(job_id, "OK")
        return job_id, result
    except Exception as e:
        fail_job(job_id, str(e))
        return job_id, None


if __name__ == "__main__":
    while True:
        text = input("DARK8 (CEL) > ").strip()

        shell = handle_shell_like(text)
        if shell:
            intent, result = shell
            print(f"[{intent}] {result}")
            continue

        mem = interactive_memory_commands(text)
        if mem:
            intent, result = mem
            print(f"[{intent}] {result}")
            continue

        jobs_cmd = interactive_jobs_commands(text)
        if jobs_cmd:
            intent, result = jobs_cmd
            print(f"[{intent}] {result}")
            continue

        if text.startswith("run async:"):
            goal = text.split("run async:", 1)[1].strip()
            job_id, _ = run_agent_as_job(goal)
            print(f"[JOB] Job {job_id} uruchomiony.")
            continue

        run_agent(text)
