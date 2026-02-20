# dark8_core_paths.py
# Wspólne ścieżki i punkty odniesienia dla całego DARK8

import os

# Katalog projektu (tam, gdzie jest ten plik)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Baza systemowa DARK8 (jedna, wspólna)
DB_PATH = os.path.join(PROJECT_ROOT, "system.db")


def ensure_dirs():
    os.makedirs(PROJECT_ROOT, exist_ok=True)
