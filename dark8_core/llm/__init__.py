# DARK8 OS - Ollama LLM Integration
"""
Integration with local Ollama LLM backend for advanced reasoning.
"""

import json
from typing import AsyncGenerator, Dict, List, Optional

from dark8_core.config import config
from dark8_core.logger import logger


class OllamaClient:
    """Client for Ollama LLM backend"""

    def __init__(self, host: str = None, model: str = None):
        self.host = host or config.OLLAMA_HOST
        self.model = model or config.OLLAMA_MODEL
        self.temperature = config.OLLAMA_TEMPERATURE
        self.context_window = config.OLLAMA_CONTEXT_WINDOW
        self.available = False
        self._check_availability()

    def _check_availability(self):
        """Check if Ollama is available"""
        try:
            import asyncio

            import httpx

            async def check():
                try:
                    async with httpx.AsyncClient(timeout=5) as client:
                        response = await client.get(f"{self.host}/api/tags")
                        return response.status_code == 200
                except Exception:
                    return False

            # Run sync check
            loop = asyncio.new_event_loop()
            self.available = loop.run_until_complete(check())
            loop.close()

            if self.available:
                logger.info(f"✓ Ollama available at {self.host}")
            else:
                logger.warning(f"✗ Ollama not available at {self.host}")
        except Exception as e:
            logger.warning(f"Ollama check failed: {e}")
            self.available = False

    async def generate(self, prompt: str, context: List[int] = None) -> str:
        """
        Generate text using Ollama.

        Args:
            prompt: Text prompt
            context: Previous context window (for multi-turn)

        Returns:
            Generated text
        """
        if not self.available:
            logger.warning("Ollama not available, returning default response")
            return "Ollama is not available. Please install and start Ollama."

        try:
            import httpx

            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": self.temperature,
                "stream": False,
                "context": context or [],
            }

            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(f"{self.host}/api/generate", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
                else:
                    logger.error(f"Ollama error: {response.text}")
                    return ""
        except Exception as e:
            logger.error(f"Generate error: {e}")
            return ""

    async def generate_stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """
        Generate text with streaming response.

        Yields chunks as they arrive.
        """
        if not self.available:
            yield "Ollama is not available..."
            return

        try:
            import httpx

            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": self.temperature,
                "stream": True,
            }

            async with httpx.AsyncClient(timeout=60) as client:
                async with client.stream(
                    "POST", f"{self.host}/api/generate", json=payload
                ) as response:
                    async for line in response.aiter_lines():
                        if line:
                            data = json.loads(line)
                            chunk = data.get("response", "")
                            if chunk:
                                yield chunk
        except Exception as e:
            logger.error(f"Stream error: {e}")

    async def list_models(self) -> List[Dict]:
        """List available models"""
        try:
            import httpx

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.host}/api/tags")
                if response.status_code == 200:
                    return response.json().get("models", [])
        except Exception as e:
            logger.error(f"List models error: {e}")

        return []


class ReasoningEngine:
    """LLM-powered reasoning for agent decisions"""

    def __init__(self):
        self.client = OllamaClient()
        self.system_prompt = """You are DARK8, an autonomous AI operating system assistant.
Your role is to help users build applications, analyze code, and solve problems using natural language.
You understand Polish language well.

You should:
1. Understand the user's intent
2. Break down complex tasks into steps
3. Suggest appropriate tools and approaches
4. Provide clear explanations

Always respond in the same language as the user (Polish or English).
Be concise but informative."""

    async def reason(self, user_input: str, context: str = "") -> str:
        """
        Reason about a user command and suggest approach.

        Returns strategy/plan for execution.
        """
        prompt = f"""Context: {context}

User request: {user_input}

Analyze the request and provide:
1. What the user wants to achieve
2. Steps to accomplish it
3. Required tools or resources
4. Any potential challenges

Response (be concise):"""

        return await self.client.generate(prompt)

    async def code_review(self, code: str) -> str:
        """
        Review code and provide suggestions.
        """
        prompt = f"""Review the following code and provide feedback on:
1. Code quality
2. Potential bugs or issues
3. Performance considerations
4. Security concerns
5. Refactoring suggestions

Code:
{code}

Review (be concise):"""

        return await self.client.generate(prompt)

    async def explain_error(self, error: str, context: str = "") -> str:
        """
        Explain an error and suggest fix.
        """
        prompt = f"""A program encountered an error:

Error: {error}

Context: {context}

Please:
1. Explain what caused this error
2. Provide a solution
3. Give an example fix

Response (be concise):"""

        return await self.client.generate(prompt)


# Singleton instances
_ollama_client: Optional[OllamaClient] = None
_reasoning_engine: Optional[ReasoningEngine] = None


def get_ollama_client() -> OllamaClient:
    """Get or create Ollama client"""
    global _ollama_client
    if _ollama_client is None:
        _ollama_client = OllamaClient()
    return _ollama_client


def get_reasoning_engine() -> ReasoningEngine:
    """Get or create reasoning engine"""
    global _reasoning_engine
    if _reasoning_engine is None:
        _reasoning_engine = ReasoningEngine()
    return _reasoning_engine


__all__ = [
    "OllamaClient",
    "ReasoningEngine",
    "get_ollama_client",
    "get_reasoning_engine",
]
