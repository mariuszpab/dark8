import threading
import time

from dark8_mark01.agent.autonomic_agent import run_autonomic_task
from dark8_mark01.utils.dark8_backend import ensure_backend_ready
from dark8_mark01.utils.dark8_scheduler import start_scheduler
from dark8_mark01.utils.dark8_watchdog import start_watchdog


class Dark8CoreLoop:
    """
    DARK8‑OS Core Loop v3
    ----------------------
    Centralna pętla systemu, która:
    - pilnuje backendu LLM
    - uruchamia watchdog
    - uruchamia scheduler
    - obsługuje zadania agenta
    - zarządza stanem systemu
    """

    def __init__(self):
        self.running = False
        self.last_task = None
        self.last_result = None

    def start(self):
        """
        Uruchamia pełny system DARK8‑OS.
        """
        print("[CORE] Uruchamianie DARK8‑OS Core Loop v3...")

        # Backend musi być gotowy
        ensure_backend_ready()

        # Watchdog pilnuje backendu
        start_watchdog()

        # Scheduler wykonuje snapshoty i auto‑fix
        start_scheduler()

        self.running = True

        # Start pętli głównej w osobnym wątku
        thread = threading.Thread(target=self._loop, daemon=True)
        thread.start()

        print("[CORE] DARK8‑OS Core Loop działa w tle.")

    def _loop(self):
        """
        Główna pętla systemu.
        """
        while self.running:
            # Tu można dodać logikę monitorowania stanu systemu
            time.sleep(1)

    def run_task(self, description: str):
        """
        Uruchamia zadanie agenta w ramach OS.
        """
        print(f"[CORE] Otrzymano zadanie: {description}")

        ensure_backend_ready()

        result = run_autonomic_task(description)

        self.last_task = description
        self.last_result = result

        print("[CORE] Zadanie zakończone.")
        print("--- PLAN ---")
        print(result["plan"])
        print("--- WYNIK ---")
        print(result["result"])

        return result

    def stop(self):
        """
        Zatrzymuje pętlę systemu.
        """
        print("[CORE] Zatrzymywanie DARK8‑OS...")
        self.running = False
        print("[CORE] System zatrzymany.")
