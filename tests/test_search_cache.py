import time

import pytest

from dark8_core.search import SearchResult, SearchSource, SearchEngine


class CountingSource(SearchSource):
    def __init__(self):
        self.count = 0

    async def search(self, query: str, limit: int = 10):
        self.count += 1
        return [
            SearchResult(source="count", score=1.0, snippet=f"result {self.count}", metadata={})
        ]


@pytest.mark.asyncio
async def test_cache_hit():
    engine = SearchEngine()
    engine.cache_ttl_seconds = 5
    src = CountingSource()
    engine.register_source("count", src)

    r1 = await engine.search("q", limit=1)
    r2 = await engine.search("q", limit=1)

    assert src.count == 1
    assert r1 == r2


@pytest.mark.asyncio
async def test_cache_expiry():
    engine = SearchEngine()
    engine.cache_ttl_seconds = 1
    src = CountingSource()
    engine.register_source("count", src)

    _ = await engine.search("q", limit=1)
    assert src.count == 1

    # still cached
    _ = await engine.search("q", limit=1)
    assert src.count == 1

    # wait for expiry
    time.sleep(1.1)
    _ = await engine.search("q", limit=1)
    assert src.count == 2
