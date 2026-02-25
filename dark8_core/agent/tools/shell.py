from typing import Dict

from dark8_core.logger import logger


async def shell_execute(params: Dict) -> str:
    """Execute shell command (safe wrapper).

    Mirrors previous ToolExecutor._tool_shell_execute behavior but lives
    in a dedicated tools module so it can be reused and tested separately.
    """
    command = params.get("command")
    logger.info("[SHELL] %s", command)

    # Basic validation
    if not command or not isinstance(command, str):
        return "Error: invalid command"

    import re
    import shlex
    import subprocess

    # Disallow common shell metacharacters/operators to avoid shell injection
    if re.search(r"[;&|<>`$()]", command):
        return "Error: disallowed shell operators"

    try:
        parts = shlex.split(command)
        if not parts:
            return "Error: empty command"

        # Whitelist of allowed executables (base names)
        allowed = {"echo", "ls", "sleep", "cat", "uname"}
        base = parts[0]

        if base not in allowed:
            return f"Error: command '{base}' not allowed"

        timeout = int(params.get("timeout", 2))
        max_output = int(params.get("max_output", 1000))

        proc = subprocess.run(parts, capture_output=True, text=True, timeout=timeout)
        out = proc.stdout or proc.stderr or ""

        if len(out) > max_output:
            out = out[:max_output] + "... (truncated)"

        return out

    except subprocess.TimeoutExpired:
        return "Error: command timed out"
    except Exception as e:
        logger.exception("Shell execute error")
        return f"Error executing shell command: {e}"
