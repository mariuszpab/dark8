import os
import socket
import threading
import time

import psutil

from dark8_mark01.utils.dark8_backend import ensure_backend_ready

STATE_LOG = "dark8_logs/state_monitor.log"
CHECK_INTERVAL = 10  # sekundy


def _log(msg: str):
    os.makedirs(os.path.dirname(STATE_LOG), exist_ok=True)
    with open(STATE_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(f"[STATE] {msg}")


def _port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def _collect_system_stats():
    """
    Zbiera statystyki systemowe:
    - CPU
    - RAM
    - procesy
    """
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    processes = len(psutil.pids())

    return cpu, ram, processes


def _monitor_loop():
    """
    Główna pętla monitorowania stanu DARK8‑OS.
    """
    _log("State Monitor DARK8‑OS uruchomiony.")

    while True:
        # 1. Sprawdź backend
        backend_ok = _port_open("127.0.0.1", 11434)
        if backend_ok:
            backend_status = "OK"
        else:
            backend_status = "DOWN"
            _log("Backend LLM nie odpowiada — zgłaszam do Core Loop.")
            ensure_backend_ready()

        # 2. Statystyki systemowe
        cpu, ram, processes = _collect_system_stats()

        # 3. Zapisz stan
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        _log(f"[{timestamp}] Backend={backend_status} | CPU={cpu}% | RAM={ram}% | PROC={processes}")

        time.sleep(CHECK_INTERVAL)


def start_state_monitor():
    """
    Uruchamia monitor stanu w tle.
    """
    thread = threading.Thread(target=_monitor_loop, daemon=True)
    thread.start()
    _log("State Monitor wystartował w tle.")
