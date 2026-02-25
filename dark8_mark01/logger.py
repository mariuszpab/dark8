"""Simple logger for dark8_mark01 (ASCII-only, safe fallback)."""
try:
    from loguru import logger as _logger
except Exception:
    import logging

    _logger = logging.getLogger("dark8_mark01")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)


def log(level: str, message: str):
    lvl = (level or "INFO").upper()
    if hasattr(_logger, lvl.lower()):
        getattr(_logger, lvl.lower())(message)
    else:
        _logger.info(message)


INFO = "INFO"
WARN = "WARN"
ERROR = "ERROR"

logger = _logger
