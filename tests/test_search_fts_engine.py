import asyncio

from dark8_core.search import SearchEngine, DatabaseSearchSource
from dark8_core.agent.tools import db as db_tools


def test_search_engine_uses_fts_when_available(tmp_path):
    db_file = tmp_path / "engine_fts.db"
    db_path = str(db_file)

    # insert docs and build FTS
    id1 = db_tools.insert_document(db_path, "the quick brown fox", {})
    id2 = db_tools.insert_document(db_path, "lazy dog sleeps", {})
    assert id1 and id2
    db_tools.reindex_all(db_path)

    engine = SearchEngine()
    engine.register_source("db", DatabaseSearchSource(db_path))

    res = asyncio.run(engine.search("quick", limit=5))
    assert res.get("success") is True
    results = res.get("results", [])
    assert any(r.get("metadata", {}).get("row_id") == id1 for r in results)


def test_search_engine_falls_back_to_like_when_no_fts(tmp_path):
    db_file = tmp_path / "engine_like.db"
    db_path = str(db_file)

    # insert docs but do NOT create FTS
    id1 = db_tools.insert_document(db_path, "hello world quick", {})
    assert id1

    engine = SearchEngine()
    engine.register_source("db", DatabaseSearchSource(db_path))

    res = asyncio.run(engine.search("quick", limit=5))
    assert res.get("success") is True
    results = res.get("results", [])
    # fallback should find via LIKE
    assert any(r.get("metadata", {}).get("row_id") == id1 for r in results)
