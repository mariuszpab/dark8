class Dark8IPCMessage:
    def __init__(self, sender_pid: int, message: str):
        self.sender_pid = sender_pid
        self.message = message


class Dark8IPC:
    """
    IPC message bus dla DARK8.
    Każdy proces ma własną kolejkę wiadomości.
    """

    _instance = None

    def __init__(self):
        self.queues = {}  # pid -> list[Dark8IPCMessage]

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Dark8IPC()
        return cls._instance

    def register_pid(self, pid: int):
        if pid not in self.queues:
            self.queues[pid] = []

    def unregister_pid(self, pid: int):
        if pid in self.queues:
            del self.queues[pid]

    def send(self, sender_pid: int, target_pid: int, message: str):
        if target_pid not in self.queues:
            return False
        self.queues[target_pid].append(Dark8IPCMessage(sender_pid, message))
        return True

    def receive(self, pid: int):
        if pid not in self.queues:
            return []
        msgs = self.queues[pid][:]
        self.queues[pid].clear()
        return msgs
