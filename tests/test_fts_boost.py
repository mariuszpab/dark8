import os
import tempfile

from dark8_core.agent.tools import db


def test_fts_boost_title_over_content(tmp_path):
    db_path = tmp_path / "boost.db"
    db_path = str(db_path)

    # insert two documents:
    # doc1: title contains 'Python', content does not
    # doc2: content contains 'Python', title does not
    id1 = db.insert_document(db_path, "irrelevant content", metadata={"title": "Python guide", "tags": "lang"})
    id2 = db.insert_document(db_path, "Comprehensive Python tutorial", metadata={"title": "Guide", "tags": "lang"})

    assert id1 is not None and id2 is not None

    # Search with high title weight
    res_title_boost = db.search_fts(db_path, "Python", limit=5, weights=(5.0, 1.0, 1.0))
    assert len(res_title_boost) >= 1
    top = res_title_boost[0]
    # Expect doc1 (title match) to be ranked above doc2
    assert top.get("id") == id1

    # Search with high content weight
    res_content_boost = db.search_fts(db_path, "Python", limit=5, weights=(1.0, 5.0, 1.0))
    assert len(res_content_boost) >= 1
    top2 = res_content_boost[0]
    assert top2.get("id") == id2
