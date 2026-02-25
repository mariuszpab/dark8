from dark8_core.agent.tools import db as db_tools


def test_fts_bm25_score_exposed(tmp_path):
    db_file = tmp_path / "fts_bm25.db"
    db_path = str(db_file)

    id1 = db_tools.insert_document(db_path, "apple banana apple", {"t": "a"})
    id2 = db_tools.insert_document(db_path, "apple banana", {"t": "b"})
    assert id1 is not None and id2 is not None

    db_tools.reindex_all(db_path)
    results = db_tools.search_fts(db_path, "apple", limit=10)
    assert any("score" in r for r in results)


def test_fts_bm25_ordering(tmp_path):
    db_file = tmp_path / "fts_bm25_order.db"
    db_path = str(db_file)

    # doc1 has 'apple' twice -> should score higher
    id1 = db_tools.insert_document(db_path, "apple apple banana", {})
    id2 = db_tools.insert_document(db_path, "apple banana", {})
    db_tools.reindex_all(db_path)

    results = db_tools.search_fts(db_path, "apple", limit=2)
    assert len(results) >= 2
    # ensure scores are present and ordering is by ascending score (lower bm25 = better match)
    scores = [r.get("score") for r in results]
    assert scores[0] is not None and scores[1] is not None
    assert float(scores[0]) <= float(scores[1])


def test_fts_bm25_vs_fallback(tmp_path):
    db_file = tmp_path / "fts_bm25_vs_fallback.db"
    db_path = str(db_file)

    id1 = db_tools.insert_document(db_path, "quick brown fox jumps", {})
    id2 = db_tools.insert_document(db_path, "lazy dog sleeps", {})
    db_tools.reindex_all(db_path)

    fts = db_tools.search_fts(db_path, "quick", limit=5)
    assert any(r["id"] == id1 for r in fts)
