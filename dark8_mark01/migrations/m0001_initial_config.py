# m0001_initial_config.py
# Migracja: początkowy moduł config

import os

MIGRATION_NAME = "0001_initial_config"
VERSION = "1.0.1"


def up():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, "config.py")

    if os.path.exists(config_path):
        return

    content = """# config.py
# DARK8 OS — konfiguracja systemu

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
"""
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)


def down():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.join(base_dir, "config.py")

    if os.path.exists(config_path):
        os.remove(config_path)
