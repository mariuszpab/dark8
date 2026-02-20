class CommandRouter:
    def __init__(self):
        self.handlers = {}

    def register(self, command_type: str, handler):
        self.handlers[command_type] = handler

    def dispatch(self, task: dict, context):
        command_type = task.get("type")
        handler = self.handlers.get(command_type)
        if not handler:
            print(f"[ERROR] No handler for command type: {command_type}")
            return
        return handler(task, context)
