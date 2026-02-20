# m0003_capabilities.py
# Migracja: moduł capabilities

import os

MIGRATION_NAME = "0003_capabilities"
VERSION = "1.0.3"


def up():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    caps_path = os.path.join(base_dir, "capabilities.py")

    if os.path.exists(caps_path):
        return

    content = """# capabilities.py
# DARK8 OS — opis dostępnych możliwości systemu

CAPABILITIES = [
    \"agent: cele w języku naturalnym\",
    \"memory: projekty, cele, historia\",
    \"shell: komendy plikowe i systemowe\",
    \"jobs: procesy asynchroniczne\",
    \"meta: edycja i rozwój kodu\",
    \"chat: tryb dialogowy\",
]
"""
    with open(caps_path, "w", encoding="utf-8") as f:
        f.write(content)


def down():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    caps_path = os.path.join(base_dir, "capabilities.py")

    if os.path.exists(caps_path):
        os.remove(caps_path)
