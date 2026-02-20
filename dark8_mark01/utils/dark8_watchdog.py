import socket
import subprocess
import time
import threading
import os


OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
CHECK_INTERVAL = 5          # co ile sekund watchdog sprawdza backend
RESTART_COOLDOWN = 10       # minimalny odstęp między restartami
LOG_PATH = "dark8_logs/watchdog.log"


def _log(msg: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(f"[WATCHDOG] {msg}")


def _port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except Exception:
        return False


def _restart_backend():
    _log("Restart backendu LLM (ollama serve)...")

    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _log("Backend LLM uruchomiony ponownie.")
    except Exception as e:
        _log(f"Błąd podczas restartu backendu: {e}")


def _watchdog_loop():
    last_restart = 0

    _log("Watchdog DARK8-OS uruchomiony.")

    while True:
        alive = _port_open(OLLAMA_HOST, OLLAMA_PORT)

        if not alive:
            now = time.time()
            if now - last_restart > RESTART_COOLDOWN:
                _log("Backend LLM nie odpowiada — restartuję...")
                _restart_backend()
                last_restart = now
            else:
                _log("Backend padł, ale cooldown jeszcze trwa.")
        else:
            _log("Backend OK.")

        time.sleep(CHECK_INTERVAL)


def start_watchdog():
    """
    Uruchamia watchdog w osobnym wątku.
    """
    thread = threading.Thread(target=_watchdog_loop, daemon=True)
    thread.start()
    _log("Watchdog wystartował w tle.")
