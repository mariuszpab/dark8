"""Browser tool for DARK8_AGENT.

This tool sends JSON commands to a running browser controller (Tauri backend)
via HTTP. It's a minimal starting point; later we can add WebSocket support,
authentication, retries and richer data types.
"""
from __future__ import annotations

import json
import requests
from typing import Any, Dict, Optional

from dark8_core.logger import logger
from dark8_core.config import config


BROWSER_CONTROLLER_URL = getattr(config, "BROWSER_CONTROLLER_URL", "http://127.0.0.1:4000")


def _post(path: str, payload: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
    try:
        url = f"{BROWSER_CONTROLLER_URL.rstrip('/')}/{path.lstrip('/')}"
        r = requests.post(url, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logger.error(f"Browser tool request error: {e}")
        return {"success": False, "error": str(e)}


def browser_open_url(url: str) -> Dict[str, Any]:
    return _post("/agent/open_url", {"url": url})


def browser_get_page_content() -> Dict[str, Any]:
    return _post("/agent/get_content", {})


def browser_find(query: str) -> Dict[str, Any]:
    return _post("/agent/find", {"query": query})


def browser_download(url: str) -> Dict[str, Any]:
    return _post("/agent/download", {"url": url})


def browser_execute_js(js_code: str) -> Dict[str, Any]:
    return _post("/agent/exec_js", {"code": js_code})
