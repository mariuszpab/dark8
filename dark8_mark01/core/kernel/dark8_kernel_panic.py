from dark8_mark01.ui.system_log.dark8_system_log_bus import Dark8SystemLogBus


class Dark8KernelPanic:
    """
    DARK8 Kernel Panic Handler.
    Minimalistyczny, futurystyczny styl (C).
    """

    _instance = None

    def __init__(self):
        self.bus = Dark8SystemLogBus.instance()
        self.active = False
        self.callback = None  # shell podłączy tu funkcję wyświetlającą ekran panic

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Dark8KernelPanic()
        return cls._instance

    def trigger(self, reason: str, details: dict = None):
        if self.active:
            return  # panic już trwa

        self.active = True

        self.bus.log("KERNEL PANIC", f"Reason: {reason} | Details: {details}")

        if self.callback:
            self.callback(reason, details)

    def reset(self):
        self.active = False
