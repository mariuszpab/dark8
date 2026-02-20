from datetime import datetime


class Dark8SystemLogBus:
    """
    Prosty globalny bus logów systemowych.
    """

    _instance = None

    def __init__(self):
        self._subscribers = []
        self._history = []

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Dark8SystemLogBus()
        return cls._instance

    def subscribe(self, callback):
        self._subscribers.append(callback)
        # wyślij historię na start
        for entry in self._history:
            callback(entry)

    def log(self, source: str, message: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{ts}] [{source}] {message}"
        self._history.append(entry)
        for cb in self._subscribers:
            cb(entry)
