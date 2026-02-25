# migration_manager.py
# DARK8 OS — system migracji (SQLite)

import os
import time
from typing import List, Tuple

# Importy migracji — pełna lista
from . import m0001_initial_config, m0002_logger, m0003_capabilities, m0004_pending_actions

from dark8_core.agent.tools.db import run_query

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "system.db"))


def init_db():
    # Ensure migrations table exists via centralized DB helper
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    sql = """
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            version TEXT NOT NULL,
            applied_at TEXT NOT NULL
        )
        """
    run_query(DB_PATH, sql)


def list_available_migrations():
    return [
        (m0001_initial_config.MIGRATION_NAME, m0001_initial_config.VERSION, m0001_initial_config),
        (m0002_logger.MIGRATION_NAME, m0002_logger.VERSION, m0002_logger),
        (m0003_capabilities.MIGRATION_NAME, m0003_capabilities.VERSION, m0003_capabilities),
        (
            m0004_pending_actions.MIGRATION_NAME,
            m0004_pending_actions.VERSION,
            m0004_pending_actions,
        ),
    ]


def get_applied_migrations() -> List[Tuple[str, str]]:
    init_db()
    res = run_query(DB_PATH, "SELECT name, version FROM migrations ORDER BY id ASC")
    if not res.get("success"):
        return []
    # run_query returns rows as list of dicts with keys name/version
    return [(r.get("name"), r.get("version")) for r in res.get("rows", [])]


def get_current_version() -> str:
    applied = get_applied_migrations()
    if not applied:
        return "0.0.0"
    return applied[-1][1]


def apply_migration(name: str, version: str, module) -> str:
    init_db()
    # check if applied
    res = run_query(DB_PATH, "SELECT 1 FROM migrations WHERE name = ?", (name,))
    if res.get("success") and res.get("rows"):
        return f"Migracja {name} już zastosowana."

    # run migration module
    module.up()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    run_query(
        DB_PATH,
        "INSERT INTO migrations (name, version, applied_at) VALUES (?, ?, ?)",
        (name, version, timestamp),
    )
    return f"Zastosowano migrację: {name} (wersja {version})."


def rollback_migration(name: str, module) -> str:
    init_db()
    res = run_query(DB_PATH, "SELECT 1 FROM migrations WHERE name = ?", (name,))
    if not (res.get("success") and res.get("rows")):
        return f"Migracja {name} nie była zastosowana."

    module.down()

    run_query(DB_PATH, "DELETE FROM migrations WHERE name = ?", (name,))
    return f"Cofnięto migrację: {name}."


def upgrade_all() -> str:
    init_db()
    applied = {name for (name, _) in get_applied_migrations()}
    available = list_available_migrations()

    logs = []
    for name, version, module in available:
        if name in applied:
            logs.append(f"Pominięto {name} — już zastosowana.")
            continue
        msg = apply_migration(name, version, module)
        logs.append(msg)

    if not logs:
        return "Brak nowych migracji do zastosowania."

    return "\n".join(logs)


def status() -> str:
    init_db()
    applied = get_applied_migrations()
    available = list_available_migrations()

    lines = []
    lines.append(f"Aktualna wersja systemu: {get_current_version()}")
    lines.append("Zastosowane migracje:")

    if not applied:
        lines.append("  (brak)")
    else:
        for name, version in applied:
            lines.append(f"  - {name} (wersja {version})")

    lines.append("\nDostępne migracje:")
    for name, version, _ in available:
        marker = "[APPLIED]" if any(a[0] == name for a in applied) else "[PENDING]"
        lines.append(f"  {marker} {name} (wersja {version})")

    return "\n".join(lines)
