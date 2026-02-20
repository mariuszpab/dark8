# DARK8 OS - Agent Learning System
"""
Autonomous learning system for continuous improvement.
Learns from successful and failed tasks.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json

from dark8_core.logger import logger
from dark8_core.persistence import get_database


@dataclass
class ExecutionMetric:
    """Metrics for task execution"""
    task_id: str
    intent: str
    success: bool
    execution_time: float
    timestamp: datetime
    error: Optional[str] = None
    feedback: Optional[str] = None
    confidence_before: float = 0.5
    confidence_after: float = None


class PatternRecognition:
    """Recognize patterns in task execution"""
    
    def __init__(self):
        self.patterns: Dict[str, float] = {}
        self.anti_patterns: Dict[str, float] = {}
        self._load_patterns()
    
    def _load_patterns(self):
        """Load learned patterns from database"""
        try:
            db = get_database()
            # Fetch successful patterns
            conversations = db.get_conversations(limit=500)
            
            success_count = {}
            for conv in conversations:
                if conv.context and conv.context.get("success"):
                    key = f"{conv.intent}:{conv.user_input[:20]}"
                    success_count[key] = success_count.get(key, 0) + 1
            
            # Calculate pattern strength (how often successful)
            self.patterns = {
                k: v / 5.0 for k, v in success_count.items()
            }
            logger.info(f"✓ Loaded {len(self.patterns)} patterns")
        except Exception as e:
            logger.warning(f"Could not load patterns: {e}")
    
    def identify_pattern(self, intent: str, context: Dict) -> Optional[str]:
        """Identify applicable pattern for current task"""
        key = f"{intent}:{context.get('type', 'unknown')}"
        
        if key in self.patterns and self.patterns[key] > 0.7:
            return key
        
        return None
    
    def record_pattern(self, intent: str, context: Dict, success: bool):
        """Record pattern strength from execution"""
        key = f"{intent}:{context.get('type', 'unknown')}"
        
        if success:
            self.patterns[key] = self.patterns.get(key, 0.5) + 0.1
        else:
            self.anti_patterns[key] = self.anti_patterns.get(key, 0) + 1


class PromptOptimizer:
    """Optimize prompts based on execution results"""
    
    def __init__(self):
        self.prompt_scores: Dict[str, float] = {}
    
    def optimize_prompt(
        self,
        base_prompt: str,
        intent: str,
        success_rate: float
    ) -> str:
        """Generate optimized prompt based on success rate"""
        
        if success_rate < 0.5:
            # Add more context and examples
            return f"""{base_prompt}

Poprzednie próby: 50% sukcesów
Zalecenie: Dodaj szczegółowe kryteria akceptacji.
Przykład prawidłowego wyniku:
- Kompletna implementacja
- Testy jednostkowe
- Dokumentacja
"""
        elif success_rate < 0.8:
            # Slightly adjust phrasing
            return f"{base_prompt}\n# OczekiwanyResult: Pełna implementacja z testami"
        
        return base_prompt


class AgentLearner:
    """Main learning system for agent"""
    
    def __init__(self):
        self.pattern_recognition = PatternRecognition()
        self.prompt_optimizer = PromptOptimizer()
        self.metrics: List[ExecutionMetric] = []
        self.db = get_database()
    
    def learn_from_execution(
        self,
        task_id: str,
        intent: str,
        success: bool,
        execution_time: float,
        confidence_before: float = 0.5,
        error: Optional[str] = None,
    ) -> Dict:
        """Learn from task execution"""
        
        metric = ExecutionMetric(
            task_id=task_id,
            intent=intent,
            success=success,
            execution_time=execution_time,
            timestamp=datetime.now(),
            confidence_before=confidence_before,
            error=error,
        )
        
        self.metrics.append(metric)
        
        # Store in database
        try:
            self.db.add_audit_log(
                action=f"LEARNING:{intent}",
                parameters={"success": success, "time": execution_time},
                result="succeed" if success else "failed",
                error_message=error
            )
        except Exception as e:
            logger.warning(f"Could not log metric: {e}")
        
        return {
            "learned": True,
            "confidence_increase": 0.05 if success else -0.02,
            "metrics_recorded": len(self.metrics),
        }
    
    def get_success_rate(self, intent: str, time_window_hours: int = 24) -> float:
        """Get success rate for intent in time window"""
        
        cutoff = datetime.now() - timedelta(hours=time_window_hours)
        recent_metrics = [
            m for m in self.metrics
            if m.intent == intent and m.timestamp > cutoff
        ]
        
        if not recent_metrics:
            return 0.5
        
        successes = sum(1 for m in recent_metrics if m.success)
        return successes / len(recent_metrics)
    
    def get_average_execution_time(self, intent: str) -> float:
        """Get average execution time for intent"""
        
        metrics = [m for m in self.metrics if m.intent == intent]
        if not metrics:
            return 30.0
        
        avg = sum(m.execution_time for m in metrics) / len(metrics)
        return avg
    
    def recommend_approach(self, intent: str, context: Dict) -> Dict:
        """Recommend best approach based on learning"""
        
        success_rate = self.get_success_rate(intent)
        pattern = self.pattern_recognition.identify_pattern(intent, context)
        avg_time = self.get_average_execution_time(intent)
        
        recommendation = {
            "success_rate": success_rate,
            "recommended_pattern": pattern,
            "estimated_time": avg_time,
            "confidence": success_rate,
        }
        
        if success_rate < 0.5:
            recommendation["warning"] = "⚠️ Low success rate - use with caution"
        elif success_rate > 0.85:
            recommendation["status"] = "✓ High confidence pattern"
        
        return recommendation
    
    def get_learning_summary(self) -> Dict:
        """Get summary of learning progress"""
        
        if not self.metrics:
            return {"status": "No metrics yet"}
        
        successes = sum(1 for m in self.metrics if m.success)
        total = len(self.metrics)
        success_rate = successes / total
        
        avg_time = sum(m.execution_time for m in self.metrics) / total
        
        intents = {}
        for metric in self.metrics:
            if metric.intent not in intents:
                intents[metric.intent] = {"success": 0, "total": 0}
            intents[metric.intent]["total"] += 1
            if metric.success:
                intents[metric.intent]["success"] += 1
        
        return {
            "total_executions": total,
            "successful": successes,
            "success_rate": f"{success_rate:.1%}",
            "average_execution_time": f"{avg_time:.1f}s",
            "by_intent": intents,
            "learned_patterns": len(self.pattern_recognition.patterns),
        }


class MemoryConsolidation:
    """Consolidate and optimize memory"""
    
    @staticmethod
    def consolidate(metrics: List[ExecutionMetric]) -> Dict:
        """Consolidate metrics into knowledge"""
        
        if not metrics:
            return {}
        
        # Group by intent
        by_intent = {}
        for metric in metrics:
            if metric.intent not in by_intent:
                by_intent[metric.intent] = []
            by_intent[metric.intent].append(metric)
        
        # Generate knowledge
        knowledge = {}
        for intent, intent_metrics in by_intent.items():
            successes = sum(1 for m in intent_metrics if m.success)
            success_rate = successes / len(intent_metrics)
            
            knowledge[intent] = {
                "confidence": success_rate,
                "samples": len(intent_metrics),
                "avg_time": sum(m.execution_time for m in intent_metrics) / len(intent_metrics),
                "status": "solid" if success_rate > 0.8 else "improving" if success_rate > 0.5 else "needs work",
            }
        
        return knowledge
    
    @staticmethod
    def prune_old_memories(db, days: int = 30):
        """Remove old memories older than N days"""
        cutoff = datetime.now() - timedelta(days=days)
        logger.info(f"🗑️ Pruning memories older than {days} days")
        # Implementation would delete old records


__all__ = [
    "AgentLearner",
    "PatternRecognition",
    "PromptOptimizer",
    "MemoryConsolidation",
    "ExecutionMetric",
]
