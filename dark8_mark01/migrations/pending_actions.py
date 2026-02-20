# pending_actions.py
# Operacje na tabeli pending_actions

import sqlite3
import json
import datetime

from dark8_mark01.dark8_core_paths import DB_PATH, ensure_dirs


def _connect():
    ensure_dirs()
    return sqlite3.connect(DB_PATH)


def _ensure_table():
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


def create_pending_action(kind: str, payload: dict):
    _ensure_table()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO pending_actions (kind, payload, created_at)
        VALUES (?, ?, ?)
        """,
        (kind, json.dumps(payload), datetime.datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_latest_pending_action():
    _ensure_table()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, kind, payload, created_at
        FROM pending_actions
        ORDER BY id DESC
        LIMIT 1
        """
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "kind": row[1],
        "payload": json.loads(row[2]),
        "created_at": row[3],
    }


def delete_pending_action(action_id: int):
    _ensure_table()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM pending_actions WHERE id = ?", (action_id,))
    conn.commit()
    conn.close()
