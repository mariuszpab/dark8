# planner.py
# DARK8 OS — AGENT LAYER: planner celów → plan kroków

from dark8_mark01.memory.memory_manager import remember_project


def _normalize_goal(goal: str) -> str:
    return goal.strip().lower()


def _python_project_path(goal: str) -> str:
    return "projekty/app_python_cli"


def _web_project_path(goal: str) -> str:
    return "projekty/app_web"


def _api_project_path(goal: str) -> str:
    return "projekty/app_api"


def plan_from_goal(goal: str) -> list[dict]:
    """
    Przyjmuje cel w języku naturalnym i zwraca listę kroków.
    Każdy krok: {"intent": "...", "args": {...}, "description": "..."}
    """
    g = _normalize_goal(goal)
    steps: list[dict] = []

    # --- PROSTA APLIKACJA W PYTHONIE (CLI) ---
    if "aplikację" in g and "python" in g and ("konsol" in g or "terminal" in g or "prosta" in g):
        project_path = _python_project_path(goal)

        steps.append(
            {
                "intent": "CREATE_PROJECT",
                "args": {"path": project_path, "template": "python"},
                "description": "Tworzenie projektu aplikacji konsolowej w Pythonie",
            }
        )

        steps.append(
            {
                "intent": "GENERATE_CODE",
                "args": {
                    "language": "python",
                    "prompt": f"Stwórz prostą aplikację konsolową w Pythonie zgodną z celem: {goal}",
                },
                "description": "Generowanie kodu aplikacji konsolowej",
            }
        )

        steps.append(
            {
                "intent": "OVERWRITE_FILE",
                "args": {
                    "path": f"{project_path}/main.py",
                    "content": "# TODO: tutaj wstawimy wygenerowany kod (kolejna wersja codegen)\n",
                },
                "description": "Zapisanie kodu do pliku main.py",
            }
        )

        steps.append(
            {
                "intent": "BUILD_PROJECT",
                "args": {"path": f"{project_path}/main.py"},
                "description": "Uruchomienie aplikacji konsolowej",
            }
        )

        remember_project(project_path)
        return steps

    # --- APLIKACJA WEBOWA ---
    if "aplikację" in g and ("web" in g or "stronę" in g or "frontend" in g):
        project_path = _web_project_path(goal)

        steps.append(
            {
                "intent": "CREATE_PROJECT",
                "args": {"path": project_path, "template": "web"},
                "description": "Tworzenie projektu aplikacji webowej",
            }
        )

        steps.append(
            {
                "intent": "GENERATE_CODE",
                "args": {
                    "language": "html",
                    "prompt": f"Stwórz prostą stronę web zgodną z celem: {goal}",
                },
                "description": "Generowanie kodu HTML dla aplikacji webowej",
            }
        )

        steps.append(
            {
                "intent": "OVERWRITE_FILE",
                "args": {
                    "path": f"{project_path}/index.html",
                    "content": "<!-- TODO: tutaj wstawimy wygenerowany kod HTML -->",
                },
                "description": "Zapisanie kodu HTML do pliku index.html",
            }
        )

        remember_project(project_path)
        return steps

    # --- API / BACKEND ---
    if "api" in g or "backend" in g:
        project_path = _api_project_path(goal)

        steps.append(
            {
                "intent": "CREATE_PROJECT",
                "args": {"path": project_path, "template": "python"},
                "description": "Tworzenie projektu backend/API w Pythonie",
            }
        )

        steps.append(
            {
                "intent": "GENERATE_CODE",
                "args": {
                    "language": "python",
                    "prompt": f"Stwórz prosty backend/API w Pythonie zgodny z celem: {goal}",
                },
                "description": "Generowanie kodu backendu/API",
            }
        )

        steps.append(
            {
                "intent": "OVERWRITE_FILE",
                "args": {
                    "path": f"{project_path}/main.py",
                    "content": "# TODO: tutaj wstawimy wygenerowany kod backendu/API\n",
                },
                "description": "Zapisanie kodu backendu do pliku main.py",
            }
        )

        steps.append(
            {
                "intent": "BUILD_PROJECT",
                "args": {"path": f"{project_path}/main.py"},
                "description": "Uruchomienie backendu/API",
            }
        )

        remember_project(project_path)
        return steps

    # --- OGÓLNY CEL „STWÓRZ APLIKACJĘ” ---
    if "aplikację" in g:
        project_path = "projekty/app_generic"

        steps.append(
            {
                "intent": "CREATE_PROJECT",
                "args": {"path": project_path, "template": "default"},
                "description": "Tworzenie ogólnego projektu aplikacji",
            }
        )

        steps.append(
            {
                "intent": "GENERATE_CODE",
                "args": {
                    "language": "python",
                    "prompt": f"Stwórz szkic aplikacji zgodnej z celem: {goal}",
                },
                "description": "Generowanie szkicu aplikacji",
            }
        )

        steps.append(
            {
                "intent": "OVERWRITE_FILE",
                "args": {
                    "path": f"{project_path}/main.py",
                    "content": "# TODO: szkic aplikacji wygenerowany przez DARK8\n",
                },
                "description": "Zapisanie szkicu aplikacji",
            }
        )

        remember_project(project_path)
        return steps

    # --- BRAK DOPASOWANIA: fallback ---
    steps.append(
        {
            "intent": "LOG",
            "args": {},
            "description": f"Brak zdefiniowanego planu dla celu: {goal}",
        }
    )

    return steps
