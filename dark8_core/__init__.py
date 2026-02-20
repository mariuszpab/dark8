"""
DARK8 OS - Core Package
Autonomous AI Operating System
"""

__version__ = "0.1.0-alpha"
__author__ = "Mariusz"
__description__ = "Autonomous AI Operating System - Build applications with natural language"

"""Lightweight package initializer.

Avoid importing heavy submodules (like `config` which may require optional
dependencies such as `python-dotenv`) at import time so tools/scripts can
import parts of the package without installing all optional dependencies.
"""

__version__ = "0.1.0-alpha"
__author__ = "Mariusz"


def get_config():
    """Lazily import and return package config.

    Use this instead of importing `config` at module import time.
    """
    from .config import config as _config
    return _config


def get_logger():
    """Lazily import and return the package logger.

    Avoids importing logging machinery until required.
    """
    from .logger import logger as _logger
    return _logger


__all__ = ["get_config", "get_logger"]
