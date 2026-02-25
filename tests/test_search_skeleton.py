import pytest

from dark8_core.search import SearchEngine, FileSearchSource


@pytest.mark.asyncio
async def test_search_engine_register_and_file_search(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    f = docs / "note.txt"
    f.write_text("hello skeleton search test")

    engine = SearchEngine()
    fs = FileSearchSource(paths=[str(docs)])
    engine.register_source("files", fs)

    res = await engine.search("skeleton")
    assert res["success"] is True
    assert any(r["source"] == "file" for r in res["results"])
