from dark8_core.agent.tools import db as db_tools


def test_auto_index_on_insert(tmp_path):
    db_file = tmp_path / "events.db"
    db_path = str(db_file)

    # insert document (should auto-index)
    doc_id = db_tools.insert_document(db_path, "autoinsert content for FTS", {})
    assert doc_id is not None

    # ensure fts built and searchable
    db_tools.reindex_all(db_path)
    results = db_tools.search_fts(db_path, "autoinsert", limit=5)
    assert any(r["id"] == doc_id for r in results)


def test_auto_delete_from_fts(tmp_path):
    db_file = tmp_path / "events_del.db"
    db_path = str(db_file)

    doc_id = db_tools.insert_document(db_path, "to be deleted content", {})
    assert doc_id is not None

    # ensure indexed
    db_tools.reindex_all(db_path)
    results = db_tools.search_fts(db_path, "deleted", limit=5)
    assert any(r["id"] == doc_id for r in results)

    # delete and ensure removed
    ok = db_tools.delete_document(db_path, doc_id)
    assert ok is True
    results2 = db_tools.search_fts(db_path, "deleted", limit=5)
    assert not any(r["id"] == doc_id for r in results2)


def test_auto_update_in_fts(tmp_path):
    db_file = tmp_path / "events_upd.db"
    db_path = str(db_file)

    doc_id = db_tools.insert_document(db_path, "old content", {})
    assert doc_id is not None

    # update content
    ok = db_tools.update_document(db_path, doc_id, "new updated content", {})
    assert ok is True

    db_tools.reindex_all(db_path)
    results = db_tools.search_fts(db_path, "updated", limit=5)
    assert any(r["id"] == doc_id for r in results)
