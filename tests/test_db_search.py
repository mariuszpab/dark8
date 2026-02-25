import sqlite3

import pytest

from dark8_core.search import SearchEngine, DatabaseSearchSource, FileSearchSource


@pytest.mark.asyncio
async def test_db_search_exact(tmp_path):
    db = tmp_path / "data.db"
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    cur.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, content TEXT)")
    cur.execute("INSERT INTO documents (content) VALUES (?)", ("this contains the needle exact",))
    conn.commit()
    conn.close()

    engine = SearchEngine()
    ds = DatabaseSearchSource(str(db))
    engine.register_source("db", ds)

    res = await engine.search("needle", limit=5)
    assert res["success"] is True
    assert any(r["source"] == "db" for r in res["results"])


@pytest.mark.asyncio
async def test_db_search_fuzzy(tmp_path):
    db = tmp_path / "data2.db"
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    cur.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, content TEXT)")
    cur.execute("INSERT INTO documents (content) VALUES (?)", ("findme in database",))
    cur.execute("INSERT INTO documents (content) VALUES (?)", ("partial findmeish text",))
    conn.commit()
    conn.close()

    engine = SearchEngine()
    ds = DatabaseSearchSource(str(db))
    engine.register_source("db", ds)

    res = await engine.search("findme", limit=10)
    assert res["success"] is True
    results = res["results"]
    assert len(results) >= 1
    # best score first
    assert results[0]["score"] >= results[-1]["score"]


@pytest.mark.asyncio
async def test_db_search_no_results(tmp_path):
    db = tmp_path / "data3.db"
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    cur.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, content TEXT)")
    cur.execute("INSERT INTO documents (content) VALUES (?)", (("unrelated"),))
    conn.commit()
    conn.close()

    engine = SearchEngine()
    ds = DatabaseSearchSource(str(db))
    engine.register_source("db", ds)

    res = await engine.search("nope", limit=5)
    assert res["success"] is True
    assert res["results"] == []


@pytest.mark.asyncio
async def test_db_search_ranking_combined(tmp_path):
    # DB with one exact and one partial
    db = tmp_path / "data4.db"
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    cur.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, content TEXT)")
    cur.execute("INSERT INTO documents (content) VALUES (?)", ("exact match sample",))
    cur.execute("INSERT INTO documents (content) VALUES (?)", ("partial sample extra",))
    conn.commit()
    conn.close()

    # File with exact match as well
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.txt").write_text("exact match sample from file")

    engine = SearchEngine()
    ds = DatabaseSearchSource(str(db))
    fs = FileSearchSource(paths=[str(docs)])
    engine.register_source("db", ds)
    engine.register_source("files", fs)

    res = await engine.search("exact match", limit=5)
    assert res["success"] is True
    results = res["results"]
    assert len(results) >= 1
    # ensure ranking order (highest score first)
    assert results[0]["score"] >= results[-1]["score"]
