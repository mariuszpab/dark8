import importlib

from dark8_core.agent import get_agent


def test_plugin_registration_and_search():
    agent = get_agent()

    # import and register plugin
    mod = importlib.import_module("dark8_core.plugins.sample_search_plugin")
    mod.register(agent)

    # execute search via executor which delegates to agent.search
    res = agent.executor.execute("search", {"query": "hello", "limit": 5})

    # executor.execute returns awaitable; in this test we call result synchronously
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    out = loop.run_until_complete(res)

    assert out["success"] is True
    assert any(r["source"] == "plugin" for r in out["results"])
