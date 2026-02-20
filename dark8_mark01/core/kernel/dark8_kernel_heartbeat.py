import threading
import time


class Dark8KernelHeartbeat:
    """
    Pseudo-kernel heartbeat DARK8.
    Wywołuje callback w stałych odstępach czasu.
    """

    def __init__(self, interval_sec=1.0):
        self.interval = interval_sec
        self._running = False
        self._thread = None
        self._subscribers = []

    def subscribe(self, callback):
        """
        callback() będzie wywoływany co tick.
        """
        self._subscribers.append(callback)

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            for cb in self._subscribers:
                try:
                    cb()
                except Exception:
                    # tu można kiedyś dodać log błędów kernela
                    pass
            time.sleep(self.interval)
