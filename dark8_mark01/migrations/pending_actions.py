# pending_actions.py
# Operacje na tabeli pending_actions

import datetime
import json

from dark8_mark01.dark8_core_paths import DB_PATH, ensure_dirs
from dark8_core.agent.tools.db import run_query


def _ensure_table():
    ensure_dirs()
    sql = """
        CREATE TABLE IF NOT EXISTS pending_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    run_query(DB_PATH, sql)


def create_pending_action(kind: str, payload: dict):
    _ensure_table()
    run_query(
        DB_PATH,
        "INSERT INTO pending_actions (kind, payload, created_at) VALUES (?, ?, ?)",
        (kind, json.dumps(payload), datetime.datetime.utcnow().isoformat()),
    )


def get_latest_pending_action():
    _ensure_table()
    res = run_query(
        DB_PATH,
        """
        SELECT id, kind, payload, created_at
        FROM pending_actions
        ORDER BY id DESC
        LIMIT 1
        """,
    )
    rows = res.get("rows", []) if res.get("success") else []
    if not rows:
        return None
    row = rows[0]
    return {
        "id": row.get("id"),
        "kind": row.get("kind"),
        "payload": json.loads(row.get("payload") or "null"),
        "created_at": row.get("created_at"),
    }


def delete_pending_action(action_id: int):
    _ensure_table()
    run_query(DB_PATH, "DELETE FROM pending_actions WHERE id = ?", (action_id,))
