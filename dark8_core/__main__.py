# DARK8 OS - Main Entry Point
"""
DARK8 OS main entry point.
Usage: python -m dark8_core [--mode cli|api|browser]
"""

import sys
import asyncio

from dark8_core.logger import logger
from dark8_core.config import config
from dark8_core.boot import boot


async def run_cli_mode():
    """Run in CLI Agent mode"""
    logger.info("🖤 CLI Agent mode")
    
    from dark8_core.agent import get_agent
    
    agent = get_agent()
    await agent.run()


async def run_api_mode():
    """Run in API Server mode"""
    logger.info(f"🖤 API Server mode (:{config.API_PORT})")
    
    try:
        import uvicorn
        from dark8_core.ui.api import app
        
        config_dict = {
            'host': config.API_HOST,
            'port': config.API_PORT,
            'log_level': 'info' if not config.DEBUG else 'debug',
            'reload': config.API_RELOAD,
        }
        
        await asyncio.to_thread(uvicorn.run, app, **config_dict)
    except Exception as e:
        logger.error(f"API Server error: {e}")


async def run_browser_mode():
    """Run in Browser mode"""
    logger.info("🖤 Browser mode")
    logger.info("Browser not yet implemented")


async def main_async(mode: str = "cli"):
    """Main async entry point"""
    
    # Boot system
    _agent = await boot()
    
    # Route to mode
    if mode == "cli":
        await run_cli_mode()
    elif mode == "api":
        await run_api_mode()
    elif mode == "browser":
        await run_browser_mode()
    else:
        logger.error(f"Unknown mode: {mode}")
        sys.exit(1)


def main():
    """Main entry point"""
    try:
        # Parse arguments
        mode = "cli"
        if "--mode" in sys.argv:
            idx = sys.argv.index("--mode")
            if idx + 1 < len(sys.argv):
                mode = sys.argv[idx + 1]
        
        # Run async main
        asyncio.run(main_async(mode))
        
    except KeyboardInterrupt:
        logger.info("\nShutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
