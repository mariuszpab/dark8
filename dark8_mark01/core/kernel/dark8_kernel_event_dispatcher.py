from dark8_mark01.ui.system_log.dark8_system_log_bus import Dark8SystemLogBus


class Dark8KernelEventDispatcher:
    """
    Centralny dispatcher zdarzeń kernela DARK8.
    """

    _instance = None

    def __init__(self):
        self.bus = Dark8SystemLogBus.instance()
        self._subscribers = []

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Dark8KernelEventDispatcher()
        return cls._instance

    def subscribe(self, callback):
        """
        callback(event_dict)
        """
        self._subscribers.append(callback)

    def emit(self, event_type: str, source: str, payload: dict = None):
        """
        Emituje zdarzenie kernela.
        """
        event = {"type": event_type, "source": source, "payload": payload or {}}

        # log systemowy
        self.bus.log(f"KernelEvent:{event_type}", f"{source} → {payload}")

        # powiadom subskrybentów
        for cb in self._subscribers:
            try:
                cb(event)
            except Exception:
                pass
