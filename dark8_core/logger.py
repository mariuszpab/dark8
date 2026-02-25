# DARK8 OS - Unified Logger
# Centralized logging for entire system

import sys

from loguru import logger as loguru_logger

from dark8_core.config import config

# Remove default handler
loguru_logger.remove()

# Console output (with colors)
loguru_logger.add(
    sys.stdout,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=config.LOG_LEVEL,
    colorize=True,
)

# File output (JSON format for parsing)
log_file = config.LOG_DIR / "dark8.log"
loguru_logger.add(
    str(log_file),
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} | {message}",
    level=config.LOG_LEVEL,
    rotation="10 MB",
    retention="7 days",
)

# Export logger
logger = loguru_logger

__all__ = ["logger"]
