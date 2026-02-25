import sqlite3

import pytest

from dark8_core.agent import get_agent
from dark8_core.config import config


@pytest.mark.asyncio
async def test_search_files(tmp_path):
    p = tmp_path / "docs"
    p.mkdir()
    f = p / "a.txt"
    f.write_text("This is a needle in a haystack\nmore content")

    agent = get_agent()
    res = await agent.executor.execute(
        "search", {"query": "needle", "paths": [str(tmp_path)], "limit": 10}
    )
    assert res["success"] is True
    assert any(r["source"] == "file" for r in res["results"])


@pytest.mark.asyncio
async def test_search_db(tmp_path):
    db = tmp_path / "data.db"
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    cur.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, content TEXT)")
    cur.execute("INSERT INTO documents (content) VALUES (?)", ("findme in db",))
    conn.commit()
    conn.close()

    # point config to this DB
    config.DATABASE_URL = f"sqlite:///{db}"

    agent = get_agent()
    res = await agent.executor.execute("search", {"query": "findme", "use_db": True, "limit": 10})
    assert res["success"] is True
    assert any(r["source"] == "db" for r in res["results"])


@pytest.mark.asyncio
async def test_search_no_results(tmp_path):
    agent = get_agent()
    res = await agent.executor.execute(
        "search", {"query": "no-such-term", "paths": [str(tmp_path)], "limit": 5}
    )
    assert res["success"] is True
    assert res["results"] == []


@pytest.mark.asyncio
async def test_search_limit(tmp_path):
    for i in range(5):
        f = tmp_path / f"f{i}.txt"
        f.write_text("match here content")

    agent = get_agent()
    res = await agent.executor.execute(
        "search", {"query": "match", "paths": [str(tmp_path)], "limit": 1}
    )
    assert res["success"] is True
    assert len(res["results"]) == 1


@pytest.mark.asyncio
async def test_search_invalid_query():
    agent = get_agent()
    res = await agent.executor.execute("search", {"query": None})
    assert res["success"] is False
    assert "invalid query" in res["error"]
