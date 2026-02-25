import os
import socket
import subprocess
import time

OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
BACKEND_TIMEOUT = 2
RESTART_DELAY = 1
LOG_PATH = "dark8_logs/backend.log"


def _log(msg: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(f"[BACKEND] {msg}")


def _port_open(host: str, port: int, timeout: float = BACKEND_TIMEOUT) -> bool:
    """
    Sprawdza, czy port backendu LLM odpowiada.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def _start_backend():
    """
    Uruchamia backend LLM (ollama serve).
    """
    _log("Uruchamiam backend LLM (ollama serve)...")

    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        _log("Backend LLM wystartował.")
    except Exception as e:
        _log(f"Błąd podczas uruchamiania backendu: {e}")


def _wait_for_backend(timeout: int = 10) -> bool:
    """
    Czeka aż backend zacznie odpowiadać.
    """
    start = time.time()

    while time.time() - start < timeout:
        if _port_open(OLLAMA_HOST, OLLAMA_PORT):
            return True
        time.sleep(0.2)

    return False


def ensure_backend_ready():
    """
    Główna funkcja backendu DARK8‑OS.
    Zapewnia, że backend LLM działa i odpowiada.
    Jeśli backend nie działa — uruchamia go ponownie.
    """

    # Allow skipping backend checks in constrained/local test environments
    if os.getenv("SKIP_OLLAMA", "false").lower() == "true":
        _log("SKIP_OLLAMA set: skipping backend readiness check (test mode)")
        return True

    # 1. Sprawdź, czy backend odpowiada
    if _port_open(OLLAMA_HOST, OLLAMA_PORT):
        return True

    _log("Backend LLM nie odpowiada — próbuję uruchomić ponownie...")

    # 2. Spróbuj uruchomić backend
    _start_backend()
    time.sleep(RESTART_DELAY)

    # 3. Poczekaj aż backend zacznie odpowiadać
    if _wait_for_backend():
        _log("Backend LLM gotowy.")
        return True

    # 4. Jeśli nadal nie działa — błąd krytyczny
    _log("BŁĄD KRYTYCZNY: Backend LLM nie odpowiada po restarcie.")
    return False
