# DARK8 OS - Self-Improvement Engine
"""
Autonomous self-improvement system.
Tunes prompts, adjusts parameters, learns optimal strategies.
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class PerformanceMetric:
    """Performance metric for a strategy"""
    strategy_id: str
    success_rate: float
    avg_time: float
    error_rate: float
    confidence_score: float
    timestamp: datetime


class PromptTuner:
    """Automatically tune prompts via A/B testing"""
    
    def __init__(self):
        self.prompt_variants: Dict[str, List[str]] = {}
        self.performance_scores: Dict[str, float] = {}
    
    def create_variants(self, base_prompt: str, intent: str) -> List[str]:
        """Generate prompt variants for A/B testing"""
        
        variants = [
            # Variant 1: Original
            base_prompt,
            
            # Variant 2: More specific
            f"{base_prompt}\nBe specific and detailed.",
            
            # Variant 3: Step-by-step
            f"{base_prompt}\nProvide step-by-step solution.",
            
            # Variant 4: Examples included
            f"{base_prompt}\nInclude examples and best practices.",
            
            # Variant 5: Constraints specified
            f"{base_prompt}\nConsider security, performance, maintainability.",
        ]
        
        self.prompt_variants[intent] = variants
        return variants
    
    def select_best_variant(self, intent: str, performance_data: Dict) -> str:
        """Select best performing variant"""
        
        if intent not in self.prompt_variants:
            return ""
        
        best_variant = None
        best_score = 0
        
        for i, variant in enumerate(self.prompt_variants[intent]):
            score = performance_data.get(f"variant_{i}", 0)
            if score > best_score:
                best_score = score
                best_variant = variant
        
        return best_variant or self.prompt_variants[intent][0]
    
    def get_improvement_report(self, intent: str) -> Dict:
        """Report on prompt optimization progress"""
        
        if intent not in self.prompt_variants:
            return {"status": "not_optimized"}
        
        return {
            "intent": intent,
            "variants_tested": len(self.prompt_variants[intent]),
            "best_score": max(self.performance_scores.get(f"{intent}_v{i}", 0) 
                            for i in range(len(self.prompt_variants[intent]))),
            "optimization_status": "improving",
        }


class ParameterOptimizer:
    """Optimize system parameters automatically"""
    
    DEFAULT_PARAMS = {
        "temperature": 0.7,  # LLM temperature
        "top_k": 40,  # Top-K sampling
        "max_length": 512,  # Max output length
        "cache_size": 1000,  # Response cache
        "rate_limit": 100,  # Requests per minute
        "intent_threshold": 0.5,  # Min confidence
    }
    
    def __init__(self):
        self.current_params = self.DEFAULT_PARAMS.copy()
        self.performance_history: List[PerformanceMetric] = []
    
    def adjust_parameters(self, metrics: Dict) -> Dict:
        """Automatically adjust parameters based on metrics"""
        
        adjustments = {}
        
        # If quality is low, adjust temperature
        if metrics.get("quality_score", 0.5) < 0.4:
            adjustments["temperature"] = 0.5  # More focused
        elif metrics.get("quality_score", 0.5) > 0.9:
            adjustments["temperature"] = 0.9  # More creative
        
        # If cache hit rate is low, increase cache
        if metrics.get("cache_hit_rate", 0) < 0.3:
            adjustments["cache_size"] = int(self.current_params["cache_size"] * 1.5)
        
        # If failures are high, lower threshold
        if metrics.get("error_rate", 0) > 0.2:
            adjustments["intent_threshold"] = 0.6
        
        # Apply adjustments
        self.current_params.update(adjustments)
        
        return {
            "previous_params": {k: v for k, v in self.DEFAULT_PARAMS.items()},
            "adjusted_params": self.current_params,
            "changes": adjustments,
        }
    
    def get_optimal_params(self) -> Dict:
        """Get current optimal parameters"""
        return self.current_params.copy()


class SelfImprovementEngine:
    """Main self-improvement coordinator"""
    
    def __init__(self):
        self.prompt_tuner = PromptTuner()
        self.param_optimizer = ParameterOptimizer()
        self.improvement_history: List[Dict] = []
    
    def analyze_and_improve(self, metrics: Dict, context: Dict) -> Dict:
        """
        Analyze performance and generate improvements.
        
        Returns improvement recommendations and changes.
        """
        
        recommendation = {
            "timestamp": datetime.now().isoformat(),
            "improvements": [],
            "parameter_changes": {},
            "confidence": 0,
        }
        
        # 1. Analyze current performance
        if metrics.get("success_rate", 0) < 0.7:
            recommendation["improvements"].append({
                "type": "intent_tuning",
                "suggestion": "Optimize intent classification thresholds",
                "priority": "high",
            })
        
        # 2. Adjust parameters
        param_adjustment = self.param_optimizer.adjust_parameters(metrics)
        recommendation["parameter_changes"] = param_adjustment["changes"]
        
        # 3. Suggest prompt improvements
        intent = context.get("intent", "DEFAULT")
        if metrics.get("quality_score", 0.5) < 0.6:
            base_prompt = context.get("current_prompt", "")
            variants = self.prompt_tuner.create_variants(base_prompt, intent)
            
            recommendation["improvements"].append({
                "type": "prompt_optimization",
                "variants": len(variants),
                "suggestion": "Test prompt variants to improve quality",
                "priority": "medium",
            })
        
        # 4. Cache optimization
        if metrics.get("cache_hit_rate", 0) < 0.4:
            recommendation["improvements"].append({
                "type": "cache_tuning",
                "suggestion": "Increase cache size for better hit rate",
                "priority": "low",
            })
        
        # 5. Overall confidence
        recommendation["confidence"] = min(
            metrics.get("success_rate", 0),
            1.0 - metrics.get("error_rate", 0)
        )
        
        # Store in history
        self.improvement_history.append(recommendation)
        
        return recommendation
    
    def get_improvement_summary(self) -> Dict:
        """Get summary of improvements made"""
        
        if not self.improvement_history:
            return {"status": "no_improvements_yet"}
        
        total_attempts = len(self.improvement_history)
        successful = sum(1 for x in self.improvement_history 
                        if x.get("confidence", 0) > 0.7)
        
        return {
            "total_improvement_cycles": total_attempts,
            "successful_improvements": successful,
            "success_rate": successful / total_attempts if total_attempts > 0 else 0,
            "current_parameters": self.param_optimizer.get_optimal_params(),
            "latest_recommendation": self.improvement_history[-1] if self.improvement_history else None,
        }


__all__ = [
    "SelfImprovementEngine",
    "PromptTuner",
    "ParameterOptimizer",
    "PerformanceMetric",
]
