# m0004_pending_actions.py
# Migracja: tabela pending_actions (oczekujące operacje)

import os

from dark8_core.agent.tools.db import run_query

MIGRATION_NAME = "0004_pending_actions"
VERSION = "1.0.4"

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "system.db"))


def up():
    sql = """
        CREATE TABLE IF NOT EXISTS pending_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    run_query(DB_PATH, sql)


def down():
    run_query(DB_PATH, "DROP TABLE IF EXISTS pending_actions")
