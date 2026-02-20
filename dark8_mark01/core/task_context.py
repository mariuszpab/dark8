# task_context.py
# Kontekst wykonywania zadań DARK8

class TaskContext:
    """
    Kontekst wykonywania scenariusza .mpx:
    - root_dir projektu
    - zmienne
    - cache wyników
    - ostatni wynik taska
    """

    def __init__(self, root_dir: str = ".", variables: dict | None = None):
        self.root_dir = root_dir
        self.variables = variables or {}
        self.cache = {}
        self.last_result = None

    def set_var(self, key: str, value):
        self.variables[key] = value

    def get_var(self, key: str, default=None):
        return self.variables.get(key, default)

    def set_last_result(self, result):
        self.last_result = result

    def get_last_result(self):
        return self.last_result
