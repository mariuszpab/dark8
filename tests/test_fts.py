from dark8_core.agent.tools import db as db_tools


def test_fts_insert_and_search(tmp_path):
    db_file = tmp_path / "fts.db"
    db_path = str(db_file)

    # insert some documents
    id1 = db_tools.insert_document(
        db_path, "The quick brown fox jumps over the lazy dog", {"title": "fox"}
    )
    id2 = db_tools.insert_document(
        db_path, "A fast brown fox leaps over sleeping canine", {"title": "fast fox"}
    )

    assert id1 is not None and id2 is not None

    # ensure fts and rebuild
    res = db_tools.reindex_all(db_path)
    assert res.get("success") is True

    # search for 'quick'
    results = db_tools.search_fts(db_path, "quick", limit=5)
    assert any(r["id"] == id1 for r in results)

    # search for 'fast'
    results2 = db_tools.search_fts(db_path, "fast", limit=5)
    assert any(r["id"] == id2 for r in results2)
