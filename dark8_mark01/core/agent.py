from ..plugins import load_all_plugins
from .command_router import CommandRouter
from .context import Context
from .task_runner import TaskRunner


class Agent:
    def __init__(self):
        self.context = Context()
        self.router = CommandRouter()
        self.runner = TaskRunner(self.router, self.context)

        load_all_plugins(self.router, self.context)

    def run_tasks(self, tasks: list[dict]):
        self.runner.run(tasks)
