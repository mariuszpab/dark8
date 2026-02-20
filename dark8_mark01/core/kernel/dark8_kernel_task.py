from enum import Enum, auto


class Dark8TaskState(Enum):
    RUNNING = auto()
    SLEEPING = auto()
    STOPPED = auto()


class Dark8KernelTask:
    """
    Pojedynczy proces DARK8 (pseudo‑kernel task).
    Lekki, z priorytetem i stanem.
    """

    _next_pid = 1

    def __init__(self, name: str, priority: int = 5):
        self.pid = Dark8KernelTask._next_pid
        Dark8KernelTask._next_pid += 1

        self.name = name
        self.priority = priority  # 1 = najwyższy, 10 = najniższy
        self.state = Dark8TaskState.RUNNING

    def tick(self):
        """
        Miejsce na logikę procesu.
        Na razie pusto – ma być lekko.
        """
        if self.state != Dark8TaskState.RUNNING:
            return
        # tu w przyszłości można dodać realną logikę
