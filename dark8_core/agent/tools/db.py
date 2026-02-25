"""Database tools for agent execution.

Provides a small async-compatible wrapper around SQLite operations the
agent can call as a tool. Exposes `db_execute(params)` which accepts
an action ("bootstrap", "query", "insert") and returns a JSON-serializable
result dict.
"""
from __future__ import annotations

import json
import sqlite3
from typing import Any, Dict, List, Optional, Tuple
import threading
import time

from pathlib import Path

from dark8_core.logger import logger
from dark8_core.config import config


def _resolve_db_path(params: Dict[str, Any]) -> Optional[str]:
    # Prefer explicit param
    db_path = params.get("db_path")
    if db_path:
        return str(db_path)

    # Try config.DATABASE_URL if it follows sqlite:///path
    db_url = getattr(config, "DATABASE_URL", None)
    if isinstance(db_url, str) and db_url.startswith("sqlite:///"):
        return db_url.replace("sqlite:///", "", 1)

    # Fallback to config.DATABASE_PATH
    db_path2 = getattr(config, "DATABASE_PATH", None)
    if db_path2:
        return str(db_path2)

    return None


def _connect(path: str) -> sqlite3.Connection:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=5)
    conn.row_factory = sqlite3.Row
    return conn


# simple per-db locks to serialize schema/FTS operations
_db_locks: Dict[str, threading.RLock] = {}


def _get_db_lock(path: str) -> threading.Lock:
    if path not in _db_locks:
        _db_locks[path] = threading.RLock()
    return _db_locks[path]


def _serialize_rows(rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for r in rows:
        out.append({k: r[k] for k in r.keys()})
    return out


def bootstrap_db(db_path: str) -> Dict[str, Any]:
    """Create minimal schema required by the project.

    Currently creates a `migrations` table used by bootstrapping logic.
    """
    try:
        conn = _connect(db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS migrations (
                id TEXT PRIMARY KEY,
                applied_at TEXT
            )
            """
        )
        conn.commit()
        cur.close()
        conn.close()
        return {"success": True, "message": "bootstrapped", "path": db_path}
    except Exception as e:
        logger.error(f"DB bootstrap error: {e}")
        return {"success": False, "error": str(e)}


def run_query(db_path: str, sql: str, params: Tuple = ()) -> Dict[str, Any]:
    attempts = 0
    while True:
        try:
            conn = _connect(db_path)
            cur = conn.cursor()
            cur.execute(sql, params)
            if sql.strip().lower().startswith("select"):
                rows = cur.fetchall()
                data = _serialize_rows(rows)
                cur.close()
                conn.close()
                return {"success": True, "rows": data}

            # non-select -> commit
            conn.commit()
            affected = cur.rowcount
            cur.close()
            conn.close()
            return {"success": True, "affected": affected}
        except sqlite3.OperationalError as e:
            attempts += 1
            if attempts > 5:
                logger.error(f"DB query error: {e}")
                return {"success": False, "error": str(e)}
            time.sleep(0.05 * attempts)
            continue
        except Exception as e:
            logger.error(f"DB query error: {e}")
            return {"success": False, "error": str(e)}


def run_query_all(db_path: str, sql: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    """Return all rows for a SELECT as list of dicts (convenience wrapper)."""
    res = run_query(db_path, sql, params)
    if not res.get("success"):
        return []
    return res.get("rows", [])


def run_query_single(db_path: str, sql: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
    """Return first row for a SELECT or None."""
    rows = run_query_all(db_path, sql, params)
    return rows[0] if rows else None


def run_write(db_path: str, sql: str, params: Tuple = ()) -> Dict[str, Any]:
    """Execute a write (INSERT/UPDATE/DELETE) and return affected count."""
    attempts = 0
    while True:
        try:
            conn = _connect(db_path)
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            affected = cur.rowcount
            cur.close()
            conn.close()
            return {"success": True, "affected": affected}
        except sqlite3.OperationalError as e:
            attempts += 1
            if attempts > 5:
                logger.error(f"DB write error: {e}")
                return {"success": False, "error": str(e)}
            time.sleep(0.05 * attempts)
            continue
        except Exception as e:
            logger.error(f"DB write error: {e}")
            return {"success": False, "error": str(e)}


def ensure_documents_table(db_path: str) -> Dict[str, Any]:
    """Create the `documents` table and a simple index if missing."""
    sql = """
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        metadata TEXT
    )
    """
    res = run_query(db_path, sql)
    # create index on content for LIKE queries
    try:
        run_query(db_path, "CREATE INDEX IF NOT EXISTS idx_documents_content ON documents(content)")
    except Exception:
        pass
    return res


def ensure_fts5(db_path: str) -> Dict[str, Any]:
    """Ensure FTS5 virtual table and triggers exist for `documents` table."""
    # create virtual table
    try:
        lock = _get_db_lock(db_path)
        with lock:
            conn = _connect(db_path)
            cur = conn.cursor()
            # create a standalone FTS5 table (store content in FTS table itself)
            cur.executescript(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
                    content
                );
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            return {"success": True}
    except Exception as e:
        logger.error(f"ensure_fts5 error: {e}")
        return {"success": False, "error": str(e)}


def rebuild_fts_index(db_path: str) -> Dict[str, Any]:
    """Rebuild FTS index from `documents` table."""
    lock = _get_db_lock(db_path)
    with lock:
        try:
            conn = _connect(db_path)
            cur = conn.cursor()
            # ensure fts exists
            ensure_fts5(db_path)

            # prefer FTS5 rebuild mechanism to avoid manually manipulating
            # internal FTS tables which can lead to corruption
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='documents_fts'")
            if cur.fetchone():
                try:
                    cur.execute("INSERT INTO documents_fts(documents_fts) VALUES('rebuild')")
                except sqlite3.DatabaseError as e:
                    logger.error(f"rebuild_fts_index: rebuild failed: {e}")
                    cur.close()
                    conn.close()
                    return {"success": False, "error": str(e)}
            else:
                # no fts table, create it and let ensure_fts5 handle creation
                ensure_fts5(db_path)
            conn.commit()
            cur.close()
            conn.close()
            return {"success": True}
        except Exception as e:
            logger.error(f"rebuild_fts_index error: {e}")
            return {"success": False, "error": str(e)}


def search_fts(db_path: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search FTS5 virtual table. Returns list of dicts with id, snippet, score optional."""
    out: List[Dict[str, Any]] = []
    if not query:
        return out
    try:
        # use MATCH; snippet uses  -1 to return whole content snippet
        sql = "SELECT rowid, snippet(documents_fts, -1, '<b>', '</b>', '...', 10) as snippet FROM documents_fts WHERE documents_fts MATCH ? LIMIT ?"
        res = run_query(db_path, sql, (query, limit))
        if not res.get("success"):
            return out
        for r in res.get("rows", []):
            out.append({"id": r.get("rowid"), "snippet": r.get("snippet") or ""})
        return out
    except Exception:
        return out


def index_document(db_path: str, doc_id: int, content: str) -> bool:
    """Index a single document into documents table and FTS (insert or update)."""
    try:
        # ensure documents table
        lock = _get_db_lock(db_path)
        with lock:
            ensure_documents_table(db_path)
            existing = run_query_single(db_path, "SELECT id FROM documents WHERE id = ?", (doc_id,))
            if existing:
                run_write(db_path, "UPDATE documents SET content = ? WHERE id = ?", (content, doc_id))
            else:
                run_write(db_path, "INSERT INTO documents (id, content, metadata) VALUES (?, ?, ?)", (doc_id, content, json.dumps({})))
            # ensure FTS exists and update FTS table explicitly
            ensure_fts5(db_path)
            try:
                # replace existing FTS row for this doc
                run_write(db_path, "DELETE FROM documents_fts WHERE rowid = ?", (doc_id,))
            except Exception:
                pass
            run_write(db_path, "INSERT INTO documents_fts(rowid, content) VALUES (?, ?)", (doc_id, content))
            return True
    except Exception as e:
        logger.error(f"index_document error: {e}")
        return False


def reindex_all(db_path: str) -> Dict[str, Any]:
    """Full reindex: ensure FTS and rebuild index."""
    ensure_documents_table(db_path)
    ensure_fts5(db_path)
    return rebuild_fts_index(db_path)


def insert_document(db_path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Optional[int]:
    """Insert a document into `documents` and return inserted id."""
    ensure_documents_table(db_path)
    meta_json = json.dumps(metadata or {})
    try:
        lock = _get_db_lock(db_path)
        with lock:
            conn = _connect(db_path)
            cur = conn.cursor()
            cur.execute("INSERT INTO documents (content, metadata) VALUES (?, ?)", (content, meta_json))
            conn.commit()
            last = cur.lastrowid
            cur.close()
            conn.close()
            # Ensure FTS exists and index the inserted document
            try:
                ensure_fts5(db_path)
                index_document(db_path, last, content)
            except Exception:
                pass
        return last
    except Exception as e:
        logger.error(f"Insert document error: {e}")
        return None


def get_document_by_id(db_path: str, doc_id: int) -> Optional[Dict[str, Any]]:
    row = run_query_single(db_path, "SELECT id, content, metadata FROM documents WHERE id = ?", (doc_id,))
    if not row:
        return None
    try:
        meta = json.loads(row.get("metadata") or "{}")
    except Exception:
        meta = {}
    return {"id": row.get("id"), "content": row.get("content"), "metadata": meta}


def list_documents(db_path: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    rows = run_query_all(db_path, "SELECT id, content, metadata FROM documents ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset))
    out = []
    for r in rows:
        try:
            meta = json.loads(r.get("metadata") or "{}")
        except Exception:
            meta = {}
        out.append({"id": r.get("id"), "content": r.get("content"), "metadata": meta})
    return out


def delete_document(db_path: str, doc_id: int) -> bool:
    lock = _get_db_lock(db_path)
    with lock:
        res = run_write(db_path, "DELETE FROM documents WHERE id = ?", (doc_id,))
        # also ensure FTS row removed (triggers may handle it, but enforce)
        try:
            run_write(db_path, "DELETE FROM documents_fts WHERE rowid = ?", (doc_id,))
        except Exception:
            pass
        return bool(res.get("success") and res.get("affected", 0) > 0)


def update_document(db_path: str, doc_id: int, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
    """Update document content and metadata, and update FTS index."""
    meta_json = json.dumps(metadata or {})
    lock = _get_db_lock(db_path)
    with lock:
        res = run_write(db_path, "UPDATE documents SET content = ?, metadata = ? WHERE id = ?", (content, meta_json, doc_id))
        try:
            ensure_fts5(db_path)
            index_document(db_path, doc_id, content)
        except Exception:
            try:
                index_document(db_path, doc_id, content)
            except Exception:
                pass
        return bool(res.get("success") and res.get("affected", 0) >= 0)


async def db_execute(params: Dict[str, Any]) -> Dict[str, Any]:
    """High-level entrypoint for agent tool calls.

    Expected params:
      - action: 'bootstrap' | 'query' | 'insert' (default: 'query')
      - db_path: optional filesystem path to sqlite DB
      - sql: SQL statement for query/insert
      - params: sequence of parameters for SQL
    """
    action = params.get("action", "query")
    db_path = _resolve_db_path(params)
    if not db_path:
        return {"success": False, "error": "database path not provided"}

    if action == "bootstrap":
        return bootstrap_db(db_path)

    if action in ("query", "insert", "exec"):
        sql = params.get("sql")
        if not sql:
            return {"success": False, "error": "missing sql parameter"}
        sql_params = tuple(params.get("params", ()))
        return run_query(db_path, sql, sql_params)

    return {"success": False, "error": f"unknown action: {action}"}
