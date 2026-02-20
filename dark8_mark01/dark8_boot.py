# dark8_boot.py
# DARK8 OS — tryb systemowy / boot

import time

from dark8_mark01.agent.agent_core import (
    run_agent,
    run_agent_as_job,
    handle_shell_like,
    interactive_memory_commands,
    interactive_jobs_commands,
    mode_meta,
)

from dark8_mark01.memory.memory_manager import (
    get_projects,
    get_goals,
)

from dark8_mark01.dark8_chat import run_chat_loop


BANNER = r"""
██████╗  █████╗ ██████╗ ██╗  ██╗ █████╗ 
██╔══██╗██╔══██╗██╔══██╗██║  ██║██╔══██╗
██████╔╝███████║██████╔╝███████║███████║
██╔═══╝ ██╔══██║██╔══██╗██╔══██║██╔══██║
██║     ██║  ██║██║  ██║██║  ██║██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

        DARK8 OS — tryb systemowy
"""


def show_status():
    print("\n=== STATUS SYSTEMU ===")
    print(f"Czas systemowy: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    projects = get_projects()
    goals = get_goals()
    print(f"Liczba zapamiętanych projektów: {len(projects)}")
    print(f"Liczba zapamiętanych celów:    {len(goals)}")
    print("=======================\n")


def show_main_menu():
    print("=== DARK8 OS — MENU GŁÓWNE ===")
    print("1. Tryb AGENTA (cele)")
    print("2. Tryb SHELL (komendy)")
    print("3. Pamięć (projekty / cele)")
    print("4. Joby (procesy)")
    print("5. Meta-agent (samorozwój kodu)")
    print("6. Wyjście")
    print("7. Tryb dialogowy (chat)")
    print("===============================")


def mode_agent():
    print("\n[TRYB AGENTA] Wpisuj cele w języku naturalnym. 'exit' aby wrócić.\n")
    while True:
        text = input("AGENT (CEL) > ").strip()
        if text.lower() in ["exit", "quit"]:
            break

        if text.startswith("run async:"):
            goal = text.split("run async:", 1)[1].strip()
            job_id, _ = run_agent_as_job(goal)
            print(f"[JOB] Job {job_id} uruchomiony.")
            continue

        run_agent(text)


def mode_shell():
    print("\n[TRYB SHELL] Komendy typu dir, cd, python, rm, cp, mv, pwd, cat. 'exit' aby wrócić.\n")
    while True:
        text = input("SHELL > ").strip()
        if text.lower() in ["exit", "quit"]:
            break

        shell = handle_shell_like(text)
        if shell:
            intent, result = shell
            print(f"[{intent}] {result}")
        else:
            print("Nieznana komenda shellowa.")


def mode_memory():
    print("\n[TRYB PAMIĘCI] 'jakie projekty', 'jakie cele'. 'exit' aby wrócić.\n")
    while True:
        text = input("MEMORY > ").strip()
        if text.lower() in ["exit", "quit"]:
            break

        mem = interactive_memory_commands(text)
        if mem:
            intent, result = mem
            print(f"[{intent}] {result}")
        else:
            print("Nieznana komenda pamięci.")


def mode_jobs():
    print("\n[TRYB JOBÓW] 'jobs', 'job <id>', 'kill <id>'. 'exit' aby wrócić.\n")
    while True:
        text = input("JOBS > ").strip()
        if text.lower() in ["exit", "quit"]:
            break

        jobs_cmd = interactive_jobs_commands(text)
        if jobs_cmd:
            intent, result = jobs_cmd
            print(f"[{intent}] {result}")
        else:
            print("Nieznana komenda jobów.")


def main():
    print(BANNER)
    show_status()

    while True:
        show_main_menu()
        choice = input("Wybierz tryb: ").strip()

        if choice == "1":
            mode_agent()
        elif choice == "2":
            mode_shell()
        elif choice == "3":
            mode_memory()
        elif choice == "4":
            mode_jobs()
        elif choice == "5":
            mode_meta()
        elif choice == "6":
            print("Zamykanie DARK8 OS...")
            break
        elif choice == "7":
            run_chat_loop()
        else:
            print("Niepoprawny wybór.\n")


if __name__ == "__main__":
    main()
