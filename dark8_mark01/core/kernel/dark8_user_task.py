from dark8_mark01.core.kernel.dark8_kernel_task import Dark8KernelTask
from dark8_mark01.core.kernel.dark8_ipc_bus import Dark8IPC


class Dark8UserTask(Dark8KernelTask):
    """
    Proces użytkownika w DARK8.
    """

    def __init__(self, name: str, priority: int = 5):
        super().__init__(name, priority)
        self.userland = True

    def tick(self):
        # Odbieramy wiadomości z IPC
        msgs = Dark8IPC.instance().receive(self.pid)
        for msg in msgs:
            print(f"[IPC] PID {self.pid} received from {msg.sender_pid}: {msg.message}")
        # Tu w przyszłości można dodać logikę procesu
        return
