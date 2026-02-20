# m0002_logger.py
# Migracja: moduł logger

import os

MIGRATION_NAME = "0002_logger"
VERSION = "1.0.2"


def up():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    logger_path = os.path.join(base_dir, "logger.py")

    if os.path.exists(logger_path):
        return

    content = """# logger.py
# DARK8 OS — prosty logger

import os
import time

from .config import LOG_DIR


LEVELS = [\"INFO\", \"WARN\", \"ERROR\"]


def log(level: str, message: str):
    level = level.upper()
    if level not in LEVELS:
        level = \"INFO\"

    ts = time.strftime(\"%Y-%m-%d %H:%M:%S\")
    line = f\"[{ts}] [{level}] {message}\"

    print(line)

    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, \"dark8.log\")
    with open(log_file, \"a\", encoding=\"utf-8\") as f:
        f.write(line + \"\\n\")
"""
    with open(logger_path, "w", encoding="utf-8") as f:
        f.write(content)


def down():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    logger_path = os.path.join(base_dir, "logger.py")

    if os.path.exists(logger_path):
        os.remove(logger_path)
