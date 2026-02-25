import psutil

from dark8_mark01.core.kernel.dark8_kernel_event_dispatcher import Dark8KernelEventDispatcher


class Dark8KernelSystemMonitor:
    """
    Połączony Health Monitor + Watchdog.
    Jeden pomiar → mniej obciążenia.
    """

    def __init__(self, cpu_threshold=85, ram_threshold=90):
        self.cpu_threshold = cpu_threshold
        self.ram_threshold = ram_threshold
        self.dispatcher = Dark8KernelEventDispatcher.instance()

    def tick(self):
        cpu = psutil.cpu_percent(interval=0.0)
        ram = psutil.virtual_memory().percent

        # event informacyjny (nie spamujemy logów)
        self.dispatcher.emit("SYSTEM_STATUS", "KernelMonitor", {"cpu": cpu, "ram": ram})

        # eventy krytyczne
        if cpu >= self.cpu_threshold:
            self.dispatcher.emit(
                "CPU_HIGH", "KernelMonitor", {"cpu": cpu, "threshold": self.cpu_threshold}
            )

        if ram >= self.ram_threshold:
            self.dispatcher.emit(
                "RAM_HIGH", "KernelMonitor", {"ram": ram, "threshold": self.ram_threshold}
            )
