import asyncio
import sqlite3

from dark8_core import boot
from dark8_core.config import config


def test_initialize_database_creates_sqlite(tmp_path):
    db_file = tmp_path / "test_dark8.db"
    # Point config to temporary sqlite file
    config.DATABASE_URL = f"sqlite:///{db_file}"

    # Ensure file does not exist before
    if db_file.exists():
        db_file.unlink()

    res = asyncio.run(boot.initialize_database())
    assert res is True
    assert db_file.exists()

    # Verify migrations table exists
    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migrations'")
    row = cur.fetchone()
    conn.close()
    assert row is not None
