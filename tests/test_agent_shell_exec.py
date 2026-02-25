import pytest

from dark8_core.agent import get_agent


@pytest.mark.asyncio
async def test_do_allowed_command():
    agent = get_agent()
    res = await agent.executor.execute("shell_execute", {"command": "echo hello"})
    assert "hello" in res


@pytest.mark.asyncio
async def test_block_disallowed_command():
    agent = get_agent()
    res = await agent.executor.execute("shell_execute", {"command": "rm -rf /"})
    assert res.startswith("Error: command")


@pytest.mark.asyncio
async def test_block_shell_operators():
    agent = get_agent()
    res = await agent.executor.execute("shell_execute", {"command": "echo hi | wc -c"})
    assert "disallowed shell operators" in res


@pytest.mark.asyncio
async def test_timeout():
    agent = get_agent()
    # sleep for longer than default timeout (2s)
    res = await agent.executor.execute("shell_execute", {"command": "sleep 3"})
    assert "timed out" in res


@pytest.mark.asyncio
async def test_output_truncation():
    agent = get_agent()
    long_arg = "x" * 2000
    cmd = f"echo {long_arg}"
    res = await agent.executor.execute("shell_execute", {"command": cmd, "max_output": 500})
    assert "... (truncated)" in res
