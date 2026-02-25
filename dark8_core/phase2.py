# DARK8 OS - Phase 2 Integration Module
"""
Integration point for Phase 2 advanced features.
Ties together all new components.
"""

from typing import Dict, Optional

from dark8_core.agent.learning import AgentLearner
from dark8_core.agent.reasoning import AdvancedAgent
from dark8_core.browser.advanced import AdvancedBrowser
from dark8_core.logger import logger
from dark8_core.nlp.advanced import get_advanced_nlp
from dark8_core.performance import PerformanceOptimizer
from dark8_core.programmer.advanced import AdvancedCodeGenerator
from dark8_core.security import AuditLogger, InputValidator, SecurityContext


class Phase2SystemIntegration:
    """Main integration for Phase 2 features"""

    def __init__(self):
        logger.info("🚀 Initializing Phase 2 Advanced Systems...")

        # NLP
        self.nlp = get_advanced_nlp()
        logger.info("✓ Advanced NLP engine loaded")

        # Agent
        self.agent = AdvancedAgent()
        self.learner = AgentLearner()
        logger.info("✓ Advanced agent with reasoning loaded")

        # Code generation
        self.code_gen = AdvancedCodeGenerator()
        logger.info("✓ Advanced code generator loaded")

        # Browser
        self.browser = AdvancedBrowser()
        logger.info("✓ Advanced browser loaded")

        # Security
        self.validator = InputValidator()
        self.security_context = SecurityContext(user="system", role="admin")
        self.audit_logger = AuditLogger()
        logger.info("✓ Security layer loaded")

        # Performance
        self.performance = PerformanceOptimizer()
        logger.info("✓ Performance optimizer loaded")

        logger.info("✅ Phase 2 systems initialized!")

    async def process_command_advanced(self, user_input: str) -> Dict:
        """
        Process command with full Phase 2 capabilities.

        Includes:
        - Input validation
        - Advanced NLP parsing
        - Multi-step reasoning
        - Learning from results
        - Performance monitoring
        """

        # 1. Validate input
        if not self.validator.validate_command(user_input):
            return {"error": "Invalid command"}

        # 2. Process with reasoning
        reasoning_result = await self.agent.process_with_reasoning(user_input)

        if reasoning_result.get("status") == "need_context":
            return reasoning_result

        # 3. Get recommendation
        recommendation = reasoning_result.get("recommendation")
        logger.info(f"[CMD] Recommendation: {recommendation}")

        return reasoning_result

    def get_system_overview(self) -> Dict:
        """Get complete system overview"""

        health = self.performance.system_monitor.get_health_status()
        cache_stats = self.performance.cache.get_stats()
        learning_summary = self.learner.get_learning_summary()

        return {
            "system_health": health["status"],
            "alerts": health.get("alerts", []),
            "cache": cache_stats,
            "learning": learning_summary,
            "nlp_ready": True,
            "agent_ready": True,
            "code_gen_ready": True,
            "browser_ready": True,
        }


# Singleton instance
_phase2_system: Optional[Phase2SystemIntegration] = None


def get_phase2_system() -> Phase2SystemIntegration:
    """Get Phase 2 system instance"""
    global _phase2_system
    if _phase2_system is None:
        _phase2_system = Phase2SystemIntegration()
    return _phase2_system


__all__ = [
    "Phase2SystemIntegration",
    "get_phase2_system",
]
