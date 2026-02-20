# dark8_self_repair.py
# Warstwa self-repair dla DARK8

import os
import sqlite3

from dark8_mark01.dark8_core_paths import DB_PATH, ensure_dirs
from dark8_mark01.migrations import migration_manager
from dark8_mark01.dark8_self_diagnostics import full_diagnostics


def ensure_db_exists():
    ensure_dirs()
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.close()
    migration_manager.init_db()


def ensure_pending_actions_table():
    conn = sqlite3.connect(DB_PATH)
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


def force_migrations():
    return migration_manager.upgrade_all()


def self_repair():
    """
    Wykonuje podstawową sekwencję naprawczą:
    - upewnia się, że baza istnieje
    - upewnia się, że tabela pending_actions istnieje
    - wykonuje wszystkie migracje
    - zwraca raport
    """
    ensure_db_exists()
    ensure_pending_actions_table()
    mig_log = force_migrations()
    diag = full_diagnostics()

    return {
        "migrations_log": mig_log,
        "diagnostics_after": diag,
    }
