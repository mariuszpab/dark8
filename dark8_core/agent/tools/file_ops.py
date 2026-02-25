from typing import Dict

from dark8_core.logger import logger


async def file_read(params: Dict) -> str:
    """Read a file and return up to first 500 characters."""
    file_path = params.get("path")
    try:
        with open(file_path, "r") as f:
            return f.read()[:500]
    except Exception as e:
        logger.exception("File read error")
        return f"Error reading file: {e}"


async def file_write(params: Dict) -> str:
    """Write `content` to a file at `path` and return a confirmation."""
    file_path = params.get("path")
    content = params.get("content", "")
    try:
        with open(file_path, "w") as f:
            f.write(content)
        return f"✓ File written: {file_path}"
    except Exception as e:
        logger.exception("File write error")
        return f"Error writing file: {e}"
