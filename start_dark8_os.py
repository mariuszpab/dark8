import time

from dark8_mark01.utils.dark8_backend import ensure_backend_ready
from dark8_mark01.utils.dark8_watchdog import start_watchdog
from dark8_mark01.utils.dark8_scheduler import start_scheduler
from dark8_mark01.utils.dark8_state_monitor import start_state_monitor
from dark8_mark01.core.dark8_core_loop import Dark8CoreLoop


def main():
    print("[START] DARK8‑OS — tryb headless (bez UI)")

    # 1. Upewnij się, że backend LLM działa
    backend_ok = ensure_backend_ready()
    if not backend_ok:
        print("[START] Błąd krytyczny: backend LLM nie działa. Sprawdź logi w dark8_logs/backend.log")
        return

    # 2. Uruchom watchdog backendu
    start_watchdog()

    # 3. Uruchom scheduler (snapshoty, auto‑fix)
    start_scheduler()

    # 4. Uruchom state monitor (CPU/RAM/backend)
    start_state_monitor()

    # 5. Uruchom Core Loop (centralna pętla OS)
    core = Dark8CoreLoop()
    core.start()

    print("[START] DARK8‑OS działa w tle.")
    print("[START] Aby zakończyć, przerwij proces (Ctrl+C).")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[STOP] Przerwano przez użytkownika. Zatrzymuję DARK8‑OS...")
        core.stop()
        print("[STOP] Zakończono.")


if __name__ == "__main__":
    main()
