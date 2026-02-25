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
        title TEXT,
        content TEXT NOT NULL,
        tags TEXT,
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
            # create a standalone FTS5 table with columns for boosting
            cur.executescript(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
                    title, content, tags
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


def search_fts(
    db_path: str, query: str, limit: int = 10, weights: Optional[Tuple[float, float, float]] = None
) -> List[Dict[str, Any]]:
    """Search FTS5 virtual table. Supports optional BM25 weights tuple (title, content, tags).

    Returns list of dicts with id, snippet, score.
    """
    out: List[Dict[str, Any]] = []
    if not query:
        return out
    if weights is None:
        weights = (1.0, 1.0, 1.0)
    try:
        # use MATCH; include bm25() score with per-column weights and snippet
        sql = (
            "SELECT rowid, bm25(documents_fts, ?, ?, ?) AS score, "
            "snippet(documents_fts, -1, '<b>', '</b>', '...', 10) as snippet "
            "FROM documents_fts WHERE documents_fts MATCH ? ORDER BY score ASC LIMIT ?"
        )
        params = (weights[0], weights[1], weights[2], query, limit)
        res = run_query(db_path, sql, params)
        if not res.get("success"):
            return out
        for r in res.get("rows", []):
            out.append({"id": r.get("rowid"), "snippet": r.get("snippet") or "", "score": r.get("score")})
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
            existing = run_query_single(db_path, "SELECT id, title, metadata, tags FROM documents WHERE id = ?", (doc_id,))
            title = ""
            tags = ""
            if existing:
                # update content only if provided
                run_write(db_path, "UPDATE documents SET content = ? WHERE id = ?", (content, doc_id))
                title = existing.get("title") or ""
                tags = existing.get("tags") or ""
            else:
                # insert with empty title/tags
                run_write(db_path, "INSERT INTO documents (id, content, metadata, title, tags) VALUES (?, ?, ?, ?, ?)", (doc_id, content, json.dumps({}), title, tags))
            # ensure FTS exists and update FTS table explicitly (replace row)
            ensure_fts5(db_path)
            try:
                run_write(db_path, "DELETE FROM documents_fts WHERE rowid = ?", (doc_id,))
            except Exception:
                pass
            run_write(db_path, "INSERT INTO documents_fts(rowid, title, content, tags) VALUES (?, ?, ?, ?)", (doc_id, title or "", content, tags or ""))
            return True
    except Exception as e:
        logger.error(f"index_document error: {e}")
        return False


def reindex_all(db_path: str) -> Dict[str, Any]:
    """Full reindex: ensure FTS and rebuild index."""
    ensure_documents_table(db_path)
    ensure_fts5(db_path)
    return rebuild_fts_index(db_path)


def bulk_insert_documents(
    db_path: str,
    docs: List[Tuple[str, Optional[Dict[str, Any]]]],
    reindex: bool = False,
    batch_size: int = 1000,
) -> Dict[str, Any]:
    """Insert many documents in a single transaction and update FTS.

    docs: list of (content, metadata) tuples. Returns dict with success and
    inserted_count and optionally list of ids if small.
    """
    attempts = 0
    while True:
        try:
            lock = _get_db_lock(db_path)
            with lock:
                conn = _connect(db_path)
                cur = conn.cursor()
                # ensure tables
                ensure_documents_table(db_path)
                ensure_fts5(db_path)

                inserted_ids: List[int] = []
                # do all inserts in one transaction for speed
                for content, metadata in docs:
                    meta_json = json.dumps(metadata or {})
                    title = ""
                    tags = ""
                    try:
                        title = (metadata or {}).get("title") or ""
                        tags = (metadata or {}).get("tags") or ""
                    except Exception:
                        title = ""
                        tags = ""

                    cur.execute("INSERT INTO documents (title, content, tags, metadata) VALUES (?, ?, ?, ?)", (title, content, tags, meta_json))
                    # index into standalone FTS table explicitly using last_insert_rowid()
                    last_id = cur.lastrowid
                    cur.execute("INSERT INTO documents_fts(rowid, title, content, tags) VALUES (?, ?, ?, ?)", (last_id, title or "", content, tags or ""))
                    inserted_ids.append(last_id)

                conn.commit()
                cur.close()
                conn.close()

                if reindex:
                    # full rebuild if requested
                    reindex_all(db_path)

                return {"success": True, "inserted": len(inserted_ids), "ids": inserted_ids}
        except sqlite3.OperationalError as e:
            attempts += 1
            if attempts > 5:
                logger.error(f"bulk_insert_documents error: {e}")
                return {"success": False, "error": str(e)}
            time.sleep(0.05 * attempts)
            continue
        except Exception as e:
            logger.error(f"bulk_insert_documents error: {e}")
            return {"success": False, "error": str(e)}


def insert_document(db_path: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Optional[int]:
    """Insert a document into `documents` and return inserted id."""
    ensure_documents_table(db_path)
    meta_json = json.dumps(metadata or {})
    try:
        lock = _get_db_lock(db_path)
        with lock:
            # extract optional title/tags from metadata
            title = ""
            tags = ""
            try:
                title = (metadata or {}).get("title") or ""
                tags = (metadata or {}).get("tags") or ""
            except Exception:
                title = ""
                tags = ""

            conn = _connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO documents (title, content, tags, metadata) VALUES (?, ?, ?, ?)",
                (title, content, tags, meta_json),
            )
            conn.commit()
            last = cur.lastrowid
            cur.close()
            conn.close()
            # Ensure FTS exists and index the inserted document
            try:
                ensure_fts5(db_path)
                run_write(db_path, "INSERT INTO documents_fts(rowid, title, content, tags) VALUES (?, ?, ?, ?)", (last, title or "", content, tags or ""))
            except Exception:
                pass
        return last
    except Exception as e:
        logger.error(f"Insert document error: {e}")
        return None


def get_document_by_id(db_path: str, doc_id: int) -> Optional[Dict[str, Any]]:
    row = run_query_single(db_path, "SELECT id, title, content, tags, metadata FROM documents WHERE id = ?", (doc_id,))
    if not row:
        return None
    try:
        meta = json.loads(row.get("metadata") or "{}")
    except Exception:
        meta = {}
    return {
        "id": row.get("id"),
        "title": row.get("title"),
        "content": row.get("content"),
        "tags": row.get("tags"),
        "metadata": meta,
    }


def list_documents(db_path: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    rows = run_query_all(
        db_path, "SELECT id, title, content, tags, metadata FROM documents ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset)
    )
    out = []
    for r in rows:
        try:
            meta = json.loads(r.get("metadata") or "{}")
        except Exception:
            meta = {}
        out.append(
            {"id": r.get("id"), "title": r.get("title"), "content": r.get("content"), "tags": r.get("tags"), "metadata": meta}
        )
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
    """Update document content and metadata, update title/tags, and sync FTS index."""
    meta_json = json.dumps(metadata or {})
    lock = _get_db_lock(db_path)
    with lock:
        # update main document
        res = run_write(db_path, "UPDATE documents SET content = ?, metadata = ? WHERE id = ?", (content, meta_json, doc_id))

        # if metadata contains title/tags, update those fields too
        try:
            if metadata:
                if "title" in metadata:
                    run_write(db_path, "UPDATE documents SET title = ? WHERE id = ?", (metadata.get("title"), doc_id))
                if "tags" in metadata:
                    run_write(db_path, "UPDATE documents SET tags = ? WHERE id = ?", (metadata.get("tags"), doc_id))
        except Exception:
            pass

        # reindex into FTS: fetch current stored values to ensure consistency
        try:
            ensure_fts5(db_path)
            doc = get_document_by_id(db_path, doc_id)
            if doc is not None:
                t = doc.get("title") or ""
                c = doc.get("content") or ""
                tg = doc.get("tags") or ""
                try:
                    run_write(db_path, "DELETE FROM documents_fts WHERE rowid = ?", (doc_id,))
                except Exception:
                    pass
                run_write(db_path, "INSERT INTO documents_fts(rowid, title, content, tags) VALUES (?, ?, ?, ?)", (doc_id, t, c, tg))
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
