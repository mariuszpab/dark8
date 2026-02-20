# dark8_self_diagnostics.py
# Warstwa self-diagnostics dla DARK8

import os
import sqlite3

from dark8_mark01.dark8_core_paths import DB_PATH, PROJECT_ROOT
from dark8_mark01.migrations import migration_manager


def check_db_path():
    issues = []
    if not os.path.exists(DB_PATH):
        issues.append(f"Brak pliku bazy: {DB_PATH}")
    return {
        "db_path": DB_PATH,
        "exists": os.path.exists(DB_PATH),
        "issues": issues,
    }


def check_migrations_visibility():
    available = migration_manager.list_available_migrations()
    names = [m[0] for m in available]
    issues = []

    if "0004_pending_actions" not in names:
        issues.append("Migracja 0004_pending_actions NIE jest widoczna w migration_manager.list_available_migrations().")

    return {
        "available": names,
        "issues": issues,
    }


def check_pending_actions_table():
    issues = []
    exists = False

    if not os.path.exists(DB_PATH):
        issues.append("Baza nie istnieje, więc tabela pending_actions też nie istnieje.")
        return {"exists": False, "issues": issues}

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='pending_actions'"
    )
    row = cur.fetchone()
    conn.close()

    if row:
        exists = True
    else:
        issues.append("Brak tabeli pending_actions w bazie.")

    return {
        "exists": exists,
        "issues": issues,
    }


def full_diagnostics():
    report = {}

    report["project_root"] = PROJECT_ROOT
    report["db"] = check_db_path()
    report["migrations"] = check_migrations_visibility()
    report["pending_actions"] = check_pending_actions_table()

    return report
