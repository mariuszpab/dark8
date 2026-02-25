# DARK8 OS - Advanced Agent with Reasoning
"""
Enhanced agent with multi-step planning and reasoning.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from dark8_core.logger import logger
from dark8_core.nlp.advanced import ParsedCommand, get_advanced_nlp


@dataclass
class ExecutionPlan:
    """Represents a plan to execute a command"""

    goal: str
    steps: List[Dict]  # [{"action": "...", "params": {...}, "depends_on": [...]}]
    estimated_time: float
    risk_level: str  # low, medium, high
    rollback_plan: Optional[List[Dict]] = None


class PlanningEngine:
    """Generate execution plans from commands"""

    def __init__(self):
        self.plan_templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load pre-built execution templates"""
        return {
            "BUILD_APP": {
                "steps": [
                    {"action": "scaffold", "order": 1},
                    {"action": "generate_models", "order": 2},
                    {"action": "generate_views", "order": 3},
                    {"action": "install_deps", "order": 4},
                    {"action": "run_tests", "order": 5},
                    {"action": "package", "order": 6},
                ],
                "estimated_time": 300,  # 5 minutes
                "risk": "medium",
            },
            "DEPLOY": {
                "steps": [
                    {"action": "build_image", "order": 1},
                    {"action": "test_image", "order": 2},
                    {"action": "push_registry", "order": 3},
                    {"action": "update_service", "order": 4},
                ],
                "estimated_time": 120,
                "risk": "high",
            },
            "ANALYZE_CODE": {
                "steps": [
                    {"action": "parse_code", "order": 1},
                    {"action": "static_analysis", "order": 2},
                    {"action": "complexity_check", "order": 3},
                    {"action": "generate_report", "order": 4},
                ],
                "estimated_time": 60,
                "risk": "low",
            },
        }

    def generate_plan(self, command: ParsedCommand) -> ExecutionPlan:
        """Generate execution plan from parsed command"""

        template = self.plan_templates.get(command.intent)

        if not template:
            # Generic plan
            steps = [{"action": "execute", "params": {"intent": command.intent}}]
            estimated_time = 30
            risk = "medium"
        else:
            steps = template["steps"]
            estimated_time = template["estimated_time"]
            risk = template["risk"]

        # Adjust based on dependencies
        if command.dependencies:
            steps.insert(
                0, {"action": "resolve_dependencies", "params": {"missing": command.dependencies}}
            )
            estimated_time += 30

        return ExecutionPlan(
            goal=command.original,
            steps=steps,
            estimated_time=estimated_time,
            risk_level=risk,
            rollback_plan=self._generate_rollback_plan(command.intent),
        )

    def _generate_rollback_plan(self, intent: str) -> Optional[List[Dict]]:
        """Generate rollback plan for risky operations"""
        if intent in ["DEPLOY", "DELETE"]:
            return [
                {"action": "backup_current_state", "order": 1},
                {"action": "restore_from_backup", "order": 2},
            ]
        return None


class ReasoningAgent:
    """Agent with advanced reasoning capabilities"""

    def __init__(self):
        self.planning_engine = PlanningEngine()
        self.nlp = get_advanced_nlp()
        self.reasoning_depth = 3  # Max reasoning steps

    async def reason_about(self, user_input: str) -> Dict:
        """
        Perform multi-step reasoning about user input.

        Returns reasoning chain: {
            'command': ParsedCommand,
            'plan': ExecutionPlan,
            'alternatives': [ExecutionPlan],
            'recommendation': str,
            'confidence': float,
        }
        """

        # Step 1: Parse command
        command = self.nlp.process(user_input)
        logger.info(f"[REASON-1] Command parsed: {command.intent} ({command.confidence:.1%})")

        # Step 2: Check if more context needed
        if command.context_needed and command.dependencies:
            logger.info(f"[REASON-2] Missing context: {command.dependencies}")
            return {
                "status": "need_context",
                "command": command,
                "missing": command.dependencies,
                "suggestion": f"Please provide: {', '.join(command.dependencies)}",
            }

        # Step 3: Generate plan
        plan = self.planning_engine.generate_plan(command)
        logger.info(
            f"[REASON-3] Plan generated: {len(plan.steps)} steps, ~{plan.estimated_time}s, risk={plan.risk_level}"
        )

        # Step 4: Generate alternatives if risky
        alternatives = []
        if plan.risk_level == "high":
            alternatives = self._generate_alternatives(command, plan)
            logger.info(f"[REASON-4] Generated {len(alternatives)} alternatives")

        # Step 5: Recommendation
        recommendation = self._make_recommendation(plan, command.confidence)
        logger.info(f"[REASON-5] Recommendation: {recommendation}")

        return {
            "status": "ready",
            "command": command,
            "plan": plan,
            "alternatives": alternatives,
            "recommendation": recommendation,
            "confidence": command.confidence,
        }

    def _generate_alternatives(
        self, command: ParsedCommand, primary_plan: ExecutionPlan
    ) -> List[ExecutionPlan]:
        """Generate alternative approaches"""
        # This would generate different strategies
        # For now, return empty list
        return []

    def _make_recommendation(self, plan: ExecutionPlan, confidence: float) -> str:
        """Make recommendation based on plan quality"""
        if confidence < 0.5:
            return "⚠️ Low confidence - request clarification"
        elif plan.risk_level == "high":
            return "⚠️ High risk - enable dry-run mode before proceeding"
        else:
            return "✓ Ready to execute"


class AdvancedAgent:
    """Agent combining planning, reasoning, and execution"""

    def __init__(self):
        self.reasoning_agent = ReasoningAgent()
        self.execution_history: List[Dict] = []

    async def process_with_reasoning(self, user_input: str) -> Dict:
        """Process command with full reasoning"""

        logger.info(f"[AGENT] Processing: {user_input[:50]}...")

        # Get reasoning result
        reasoning_result = await self.reasoning_agent.reason_about(user_input)

        if reasoning_result["status"] == "need_context":
            logger.warning("Command needs more context")
            return reasoning_result

        # Ready to execute
        plan = reasoning_result["plan"]
        command = reasoning_result["command"]

        logger.info(f"[EXECUTE] Starting plan: {plan.goal}")

        # Log to history
        self.execution_history.append(
            {
                "input": user_input,
                "intent": command.intent,
                "plan_steps": len(plan.steps),
            }
        )

        return reasoning_result


__all__ = [
    "PlanningEngine",
    "ReasoningAgent",
    "AdvancedAgent",
    "ExecutionPlan",
]
