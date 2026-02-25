from dark8_core.agent.tools import db as db_tools


def test_bulk_insert_and_search(tmp_path):
    db_file = tmp_path / "bulk.db"
    db_path = str(db_file)

    docs = [
        ("apple banana", {"k": 1}),
        ("quick brown fox", {"k": 2}),
        ("lorem ipsum dolor", {"k": 3}),
    ]

    res = db_tools.bulk_insert_documents(db_path, docs)
    assert res.get("success") is True
    assert res.get("inserted") == 3

    # ensure can search
    results = db_tools.search_fts(db_path, "quick", limit=5)
    assert any(r["id"] for r in results)
