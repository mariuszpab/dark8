# DARK8 OS - REST API Server
"""
FastAPI-based REST API for DARK8 OS.
"""

import asyncio
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from dark8_core.agent import get_agent
from dark8_core.config import config
from dark8_core.logger import logger
from dark8_core.nlp import get_nlp_engine

# Create FastAPI app
app = FastAPI(
    title="DARK8 OS API",
    description="Autonomous AI Operating System API",
    version="0.1.0",
)

# Initialize components
nlp = get_nlp_engine()
agent = get_agent()


# ============================================================================
# Request/Response Models
# ============================================================================


class CommandRequest(BaseModel):
    """User command request"""

    text: str
    context: Optional[Dict] = None


class NLPResult(BaseModel):
    """NLP analysis result"""

    intent: str
    confidence: float
    entities: Dict
    tokens: List[str]


class CommandResponse(BaseModel):
    """Command execution response"""

    status: str
    response: str
    intent: str
    execution_time: float


# ============================================================================
# Health & Status Endpoints
# ============================================================================


@app.get("/")
async def root():
    """API root"""
    return {"name": "DARK8 OS", "version": "0.1.0", "status": "running", "docs": "/docs"}


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}


@app.get("/status")
async def status():
    """System status"""
    try:
        import psutil

        return {
            "environment": config.ENVIRONMENT,
            "debug": config.DEBUG,
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "agent_conversations": len(agent.memory.conversation_history),
            "agent_tasks": len(agent.memory.task_history),
        }
    except Exception as e:
        logger.error(f"Status error: {e}")
        return {"error": str(e)}


# ============================================================================
# NLP Endpoints
# ============================================================================


@app.post("/nlp/analyze", response_model=NLPResult)
async def nlp_analyze(request: CommandRequest):
    """Analyze Polish text with NLP"""
    try:
        result = nlp.understand(request.text)
        return NLPResult(
            intent=result["intent"],
            confidence=result["confidence"],
            entities=result["entities"],
            tokens=result["tokens"],
        )
    except Exception as e:
        logger.error(f"NLP error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Agent Endpoints
# ============================================================================


@app.post("/agent/command", response_model=CommandResponse)
async def agent_command(request: CommandRequest):
    """Execute command through agent"""
    import time

    try:
        start = time.time()

        # Analyze with NLP
        nlp_result = nlp.understand(request.text)

        # Execute with agent
        response = await agent.process_command(request.text, nlp_result)

        execution_time = time.time() - start

        return CommandResponse(
            status="success",
            response=response,
            intent=nlp_result["intent"],
            execution_time=execution_time,
        )
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Agent Memory Endpoints
# ============================================================================


@app.get("/agent/memory/conversations")
async def get_conversations(limit: int = 10):
    """Get recent conversations"""
    history = agent.memory.conversation_history[-limit:]
    return {"conversations": history, "total": len(agent.memory.conversation_history)}


@app.get("/agent/memory/tasks")
async def get_tasks(limit: int = 10):
    """Get recent tasks"""
    tasks = [
        {
            "id": task.id,
            "description": task.description,
            "status": task.status,
            "result": task.result,
        }
        for task in agent.memory.task_history[-limit:]
    ]
    return {"tasks": tasks, "total": len(agent.memory.task_history)}


# ============================================================================
# Configuration Endpoints
# ============================================================================


@app.get("/config")
async def get_config():
    """Get configuration (non-sensitive)"""
    return {
        "environment": config.ENVIRONMENT,
        "debug": config.DEBUG,
        "ollama_host": config.OLLAMA_HOST,
        "ollama_model": config.OLLAMA_MODEL,
        "api_host": config.API_HOST,
        "api_port": config.API_PORT,
    }


# ============================================================================
# Main
# ============================================================================


async def main():
    """Main entry for API server"""
    import uvicorn

    logger.info(f"Starting API server on {config.API_HOST}:{config.API_PORT}")

    await asyncio.to_thread(
        uvicorn.run,
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level="debug" if config.DEBUG else "info",
        reload=config.API_RELOAD,
    )


if __name__ == "__main__":
    asyncio.run(main())
