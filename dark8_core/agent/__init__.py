# DARK8 OS - Agent Core
"""
Main agent loop with reasoning and tool execution.
Integrates with Ollama LLM backend.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dark8_core.config import config
from dark8_core.logger import logger


@dataclass
class Task:
    """Represents a task to be executed"""

    id: str
    description: str
    intent: str
    entities: Dict
    priority: int = 1
    status: str = "pending"  # pending, in_progress, completed, failed
    result: Optional[str] = None


class AgentMemory:
    """Short-term and long-term memory for agent"""

    def __init__(self, max_history: int = 50):
        self.conversation_history: List[Dict] = []
        self.task_history: List[Task] = []
        self.context: Dict[str, Any] = {}
        self.max_history = max_history

    def add_interaction(self, user_input: str, ai_response: str, metadata: Dict = None):
        """Add conversation turn to history"""
        interaction = {
            "user": user_input,
            "ai": ai_response,
            "metadata": metadata or {},
        }
        self.conversation_history.append(interaction)

        # Keep only recent history
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def add_task(self, task: Task):
        """Add task to history"""
        self.task_history.append(task)

    def get_context_window(self, num_turns: int = 5) -> str:
        """Get recent context for LLM"""
        recent = self.conversation_history[-num_turns:]
        context = ""
        for turn in recent:
            context += f"User: {turn['user']}\nAI: {turn['ai']}\n\n"
        return context


class ToolExecutor:
    """Execute tools based on agent decisions"""

    def __init__(self):
        self.tools: Dict[str, callable] = {}
        self._register_builtin_tools()

    def _register_builtin_tools(self):
        """Register built-in tools"""
        # These will be implemented in separate modules
        self.tools["file_read"] = self._tool_file_read
        self.tools["file_write"] = self._tool_file_write
        self.tools["shell_execute"] = self._tool_shell_execute
        self.tools["db"] = self._tool_db_execute
        self.tools["search"] = self._tool_search

    async def execute(self, tool_name: str, parameters: Dict) -> str:
        """Execute a tool with parameters"""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found"

        try:
            result = await self.tools[tool_name](parameters)
            return result
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return f"Error executing {tool_name}: {e}"

    async def _tool_file_read(self, params: Dict) -> str:
        """Delegate file read to `agent.tools.file_ops.file_read`."""
        try:
            from .tools.file_ops import file_read
        except Exception:
            try:
                from dark8_core.agent.tools.file_ops import file_read
            except Exception:
                return "Error: file_read tool not available"

        return await file_read(params)

    async def _tool_file_write(self, params: Dict) -> str:
        """Delegate file write to `agent.tools.file_ops.file_write`."""
        try:
            from .tools.file_ops import file_write
        except Exception:
            try:
                from dark8_core.agent.tools.file_ops import file_write
            except Exception:
                return "Error: file_write tool not available"

        return await file_write(params)

    async def _tool_shell_execute(self, params: Dict) -> str:
        """Delegate to `agent.tools.shell.shell_execute` implementation."""
        try:
            from .tools.shell import shell_execute  # relative import
        except Exception:
            try:
                # fallback to absolute import
                from dark8_core.agent.tools.shell import shell_execute
            except Exception:
                return "Error: shell tool not available"

        return await shell_execute(params)

    async def _tool_db_execute(self, params: Dict) -> str:
        """Delegate DB operations to `agent.tools.db.db_execute`."""
        try:
            from .tools.db import db_execute
        except Exception:
            try:
                from dark8_core.agent.tools.db import db_execute
            except Exception:
                return {"success": False, "error": "db tool not available"}

        return await db_execute(params)

    async def _tool_search(self, params: Dict) -> str:
        """Delegate search to agent's SearchEngine if available, otherwise fallback.

        Expects params: 'query', 'limit', 'fuzzy'
        Returns dict from SearchEngine or fallback dict.
        """
        query = params.get("query")
        limit = int(params.get("limit", 10))
        fuzzy = bool(params.get("fuzzy", True))

        # Delegate to owning agent's search engine when available
        owner = getattr(self, "owner", None)
        if owner is not None and getattr(owner, "search", None) is not None:
            # build extra ephemeral sources based on params
            extra = []
            try:
                from dark8_core.search.sources import DatabaseSearchSource, FileSearchSource
            except Exception:
                FileSearchSource = None
                DatabaseSearchSource = None

            paths = params.get("paths")
            if paths and FileSearchSource is not None:
                extra.append(FileSearchSource(paths=paths))

            # support searching a provided DB by setting use_db=True
            use_db = bool(params.get("use_db", False))
            if use_db and DatabaseSearchSource is not None:
                # try to derive DB path from config.DATABASE_URL if present
                db_url = getattr(
                    __import__("dark8_core.config", fromlist=["config"]), "config"
                ).DATABASE_URL
                # expect sqlite:///path
                if isinstance(db_url, str) and db_url.startswith("sqlite:///"):
                    db_path = db_url.replace("sqlite:///", "", 1)
                    extra.append(DatabaseSearchSource(db_path))

            return await owner.search.search(query, limit=limit, fuzzy=fuzzy, extra_sources=extra)

        # Fallback: simple response
        if not query or not isinstance(query, str):
            return {"success": False, "results": [], "error": "invalid query"}

        return {"success": True, "results": [], "error": None}


class Agent:
    """DARK8 Agent - Core reasoning loop"""

    def __init__(self):
        self.memory = AgentMemory()
        self.executor = ToolExecutor()
        # allow tools to reference the owning agent
        try:
            self.executor.owner = self
        except Exception:
            pass
        # search engine for registering sources/plugins
        try:
            from dark8_core.search.engine import SearchEngine

            self.search = SearchEngine()
            # also expose on executor for convenience
            try:
                self.executor.search_engine = self.search
            except Exception:
                pass
        except Exception:
            self.search = None
        self.running = False
        logger.info("✓ Agent initialized")

    def register_search_source(self, name: str, source):
        """Register a search source with the agent's SearchEngine."""
        if getattr(self, "search", None) is None:
            raise RuntimeError("Search engine not initialized")
        self.search.register_source(name, source)

    async def process_command(self, user_input: str, nlp_result: Dict) -> str:
        """
        Process user command through full agent loop.

        Flow:
        1. UNDERSTAND (NLP already done)
        2. PLAN (decompose task)
        3. REASON (call Ollama LLM)
        4. ACT (execute tools)
        5. REFLECT (update memory)
        """
        intent = nlp_result["intent"]
        entities = nlp_result["entities"]

        logger.info(f"[AGENT] Processing intent: {intent}")

        # Step 2: PLAN
        tasks = self._plan_tasks(intent, entities, user_input)

        # Step 3: REASON (placeholder - Ollama integration)
        _decision = await self._reason_with_llm(user_input, tasks)

        # Step 4: ACT
        results = []
        for task in tasks:
            task.status = "in_progress"
            result = await self._execute_task(task)
            task.result = result
            task.status = "completed"
            results.append(result)
            self.memory.add_task(task)

        response = "\n".join(results) if results else "Task completed"

        # Step 5: REFLECT
        self.memory.add_interaction(user_input, response)

        return response

    def _plan_tasks(self, intent: str, entities: Dict, user_input: str) -> List[Task]:
        """Decompose user intent into executable tasks"""
        tasks = []

        if intent == "BUILD_APP":
            tasks.append(
                Task(
                    id="scaffold",
                    description="Generate project scaffold",
                    intent=intent,
                    entities=entities,
                )
            )
            tasks.append(
                Task(id="generate", description="Generate code", intent=intent, entities=entities)
            )
        elif intent == "SEARCH":
            tasks.append(
                Task(id="search", description="Perform search", intent=intent, entities=entities)
            )

        return tasks

    async def _reason_with_llm(self, user_input: str, tasks: List[Task]) -> Dict:
        """Call Ollama LLM for reasoning"""
        logger.info(f"[REASON] Calling Ollama at {config.OLLAMA_HOST}")

        # TODO: Implement Ollama integration
        # For now, return simple decision
        return {
            "approach": "default",
            "confidence": 0.5,
        }

    async def _execute_task(self, task: Task) -> str:
        """Execute a single task"""
        logger.info(f"[EXECUTE] Task: {task.description}")

        # Simple task execution (will be expanded)
        if task.intent == "BUILD_APP":
            return "✓ Application building not yet implemented"
        elif task.intent == "SEARCH":
            return "✓ Search not yet implemented"

        return "✓ Task executed"

    async def run(self):
        """Main agent loop"""
        self.running = True
        logger.info("🤖 Agent loop started")

        # Get NLP engine
        from dark8_core.nlp import get_nlp_engine

        nlp = get_nlp_engine()

        while self.running:
            try:
                user_input = input("\n🖤 agent> ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "stop"]:
                    logger.info("Agent shutting down...")
                    self.running = False
                    break

                # Process through NLP
                nlp_result = nlp.understand(user_input)

                if nlp_result["confidence"] < 0.3:
                    print(f"❌ Command not understood (confidence: {nlp_result['confidence']:.2%})")
                    continue

                # Process through agent
                response = await self.process_command(user_input, nlp_result)
                print(f"\n✓ {response}")

            except KeyboardInterrupt:
                logger.info("\nAgent interrupted by user")
                self.running = False
            except Exception as e:
                logger.error(f"Agent error: {e}", exc_info=True)
                print(f"❌ Error: {e}")


def get_agent() -> Agent:
    """Get or create agent singleton"""
    # This will be implemented as proper singleton
    return Agent()


__all__ = [
    "Agent",
    "Task",
    "AgentMemory",
    "ToolExecutor",
    "get_agent",
]
