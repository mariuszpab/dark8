from dark8_core.agent.tools import db as db_tools


def test_document_helpers(tmp_path):
    db_file = tmp_path / "helper.db"
    db_path = str(db_file)

    # ensure empty
    if db_file.exists():
        db_file.unlink()

    # ensure table
    res = db_tools.ensure_documents_table(db_path)
    assert res.get("success") is True

    # insert document
    doc_id = db_tools.insert_document(db_path, "hello world", {"k": "v"})
    assert isinstance(doc_id, int)

    # get by id
    doc = db_tools.get_document_by_id(db_path, doc_id)
    assert doc is not None
    assert doc["content"] == "hello world"
    assert doc["metadata"]["k"] == "v"

    # list documents
    docs = db_tools.list_documents(db_path, limit=10)
    assert len(docs) >= 1

    # delete document
    ok = db_tools.delete_document(db_path, doc_id)
    assert ok is True

    # ensure deleted
    doc2 = db_tools.get_document_by_id(db_path, doc_id)
    assert doc2 is None
