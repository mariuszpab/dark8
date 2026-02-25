import pytest

from dark8_core.search import SearchEngine, FuzzyMatcher, FileSearchSource


def test_fuzzy_exact_match():
    m = FuzzyMatcher()
    assert m.score("hello", "hello") == 1.0


def test_fuzzy_partial_match():
    m = FuzzyMatcher()
    s = m.score("hello", "well hello there")
    assert s > 0.5


def test_fuzzy_no_match():
    m = FuzzyMatcher()
    s = m.score("xyzabc", "this is unrelated text")
    assert s <= 0.3


@pytest.mark.asyncio
async def test_fuzzy_ranking(tmp_path):
    d = tmp_path / "docs"
    d.mkdir()
    (d / "a.txt").write_text("exact match sample")
    (d / "b.txt").write_text("partial match sample with extra")

    engine = SearchEngine()
    fs = FileSearchSource(paths=[str(d)])
    engine.register_source("files", fs)

    res = await engine.search("exact match", limit=2)
    assert res["success"] is True
    results = res["results"]
    assert len(results) >= 1
    # best score first
    assert results[0]["score"] >= results[-1]["score"]
