# task_runner.py
# Główny silnik wykonywania scenariuszy .mpx

from dark8_mark01.core.task_context import TaskContext
from dark8_mark01.core.task_router import TaskRouter


class TaskRunner:
    """
    Wykonuje listę tasków:
    - każdy task to dict: {"type": "...", ...}
    - wywołuje odpowiedni plugin
    - zapisuje wynik w kontekście
    """

    def __init__(self, router: TaskRouter):
        self.router = router

    def run(self, tasks: list[dict], root_dir: str = "."):
        context = TaskContext(root_dir=root_dir)

        results = []

        for task in tasks:
            result = self.router.dispatch(task, context)
            context.set_last_result(result)
            results.append(result)

        return results
