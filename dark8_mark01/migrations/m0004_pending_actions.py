# m0004_pending_actions.py
# Migracja: tabela pending_actions (oczekujące operacje)

import sqlite3
import os

MIGRATION_NAME = "0004_pending_actions"
VERSION = "1.0.4"

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "system.db"))


def _connect():
    return sqlite3.connect(DB_PATH)


def up():
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pending_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def down():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS pending_actions")
    conn.commit()
    conn.close()
