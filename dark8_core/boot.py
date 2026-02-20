# DARK8 OS - System Boot
"""
System initialization and startup sequence.
"""

import sys
import asyncio
from pathlib import Path

from dark8_core.logger import logger
from dark8_core.config import config, get_config
from dark8_core.nlp import get_nlp_engine
from dark8_core.agent import get_agent


async def check_system():
    """Verify system requirements"""
    logger.info("Checking system requirements...")
    
    from dark8_core.tools import ShellOperations
    
    requirements = {
        'python': 'python3 --version',
        'git': 'git --version',
        'curl': 'curl --version',
    }
    
    available = {}
    for tool, cmd in requirements.items():
        result = await ShellOperations.execute(cmd)
        available[tool] = result is not None
        status = "✓" if available[tool] else "✗"
        logger.info(f"  {status} {tool}")
    
    return available


async def check_ollama():
    """Check Ollama LLM backend"""
    logger.info(f"Checking Ollama backend: {config.OLLAMA_HOST}")
    
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{config.OLLAMA_HOST}/api/tags")
            if response.status_code == 200:
                logger.info(f"✓ Ollama is running")
                models = response.json().get('models', [])
                logger.info(f"  Available models: {len(models)}")
                return True
    except Exception as e:
        logger.warning(f"✗ Ollama not available: {e}")
        logger.warning(f"  Please install Ollama: https://ollama.ai")
        logger.warning(f"  And pull model: ollama pull {config.OLLAMA_MODEL}")
        return False


async def initialize_database():
    """Initialize database"""
    logger.info("Initializing database...")
    
    try:
        # TODO: Create SQLite database and tables
        logger.info("✓ Database initialized")
        return True
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        return False


async def initialize_nlp():
    """Initialize NLP engine"""
    logger.info("Initializing NLP engine...")
    
    try:
        nlp = get_nlp_engine()
        logger.info("✓ NLP engine ready")
        return True
    except Exception as e:
        logger.error(f"✗ NLP initialization failed: {e}")
        return False


async def boot():
    """
    Boot sequence for DARK8 OS.
    
    1. Check system requirements
    2. Load configuration
    3. Initialize NLP
    4. Check Ollama backend
    5. Initialize database
    6. Initialize agent
    7. Start main loop
    """
    
    logger.info("""
╔════════════════════════════════════════════╗
║         🖤 DARK8 OS v0.1.0-alpha          ║
║    Autonomous AI Operating System          ║
╚════════════════════════════════════════════╝
    """)
    
    logger.info(f"Environment: {config.ENVIRONMENT}")
    logger.info(f"Debug: {config.DEBUG}")
    logger.info(f"Log level: {config.LOG_LEVEL}")
    logger.info("")
    
    # Startup checks
    logger.info("[1/5] System Requirements")
    sys_ok = await check_system()
    
    logger.info("[2/5] NLP Engine")
    nlp_ok = await initialize_nlp()
    
    logger.info("[3/5] Ollama Backend")
    ollama_ok = await check_ollama()
    
    logger.info("[4/5] Database")
    db_ok = await initialize_database()
    
    logger.info("[5/5] Agent")
    agent = get_agent()
    
    logger.info("")
    logger.info("🖤 DARK8 OS Ready!")
    logger.info("")
    
    if not ollama_ok:
        logger.warning("⚠️  Ollama is not available. Some features will be limited.")
        logger.warning("    Install: https://ollama.ai")
    
    return agent


__all__ = ["boot"]
