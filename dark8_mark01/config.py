
"""Konfiguracja DARK8 - minimalna, bezpieczna implementacja.

Ten plik dostarcza podstawowe ścieżki i stałe używane w projekcie.
Zaimplementowany jako prosty moduł konfiguracji, można go rozszerzyć później.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LOGS_DIR = ROOT / "logs"

# Domyślne ustawienia
DEFAULTS = {
	"app_name": "DARK8",
	"version": "0.0.1",
	"data_dir": str(DATA_DIR),
	"logs_dir": str(LOGS_DIR),
}

def get(key, default=None):
	return DEFAULTS.get(key, default)

