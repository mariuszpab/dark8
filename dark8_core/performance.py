# DARK8 OS - Performance Monitoring
"""
Monitor and optimize system performance.
"""

from typing import Dict, Optional
from datetime import datetime
import psutil

from dark8_core.logger import logger


class SystemMonitor:
    """Monitor system resource usage"""
    
    def __init__(self):
        self.metrics_history: list = []
    
    def get_system_metrics(self) -> Dict:
        """Get current system metrics"""
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count(),
                },
                "memory": {
                    "percent": memory.percent,
                    "used_mb": memory.used // (1024 * 1024),
                    "available_mb": memory.available // (1024 * 1024),
                    "total_mb": memory.total // (1024 * 1024),
                },
                "disk": {
                    "percent": disk.percent,
                    "used_gb": disk.used // (1024 * 1024 * 1024),
                    "free_gb": disk.free // (1024 * 1024 * 1024),
                },
            }
            
            self.metrics_history.append(metrics)
            return metrics
        
        except Exception as e:
            logger.error(f"Could not get system metrics: {e}")
            return {}
    
    def get_health_status(self) -> Dict:
        """Get overall system health"""
        
        metrics = self.get_system_metrics()
        
        if not metrics:
            return {"status": "unknown"}
        
        alerts = []
        
        # Check thresholds
        if metrics["cpu"]["percent"] > 90:
            alerts.append(f"🔴 CPU high: {metrics['cpu']['percent']:.0f}%")
        elif metrics["cpu"]["percent"] > 70:
            alerts.append(f"🟡 CPU elevated: {metrics['cpu']['percent']:.0f}%")
        
        if metrics["memory"]["percent"] > 85:
            alerts.append(f"🔴 Memory critical: {metrics['memory']['percent']:.0f}%")
        elif metrics["memory"]["percent"] > 70:
            alerts.append(f"🟡 Memory high: {metrics['memory']['percent']:.0f}%")
        
        if metrics["disk"]["percent"] > 90:
            alerts.append(f"🔴 Disk full: {metrics['disk']['percent']:.0f}%")
        
        status = "critical" if len(alerts) > 0 else "healthy"
        
        return {
            "status": status,
            "alerts": alerts,
            "metrics": metrics,
        }


class LLMResponseCache:
    """Cache LLM responses for fast retrieval"""
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, tuple] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, prompt: str) -> Optional[str]:
        """Retrieve cached response"""
        
        key = self._hash_prompt(prompt)
        
        if key in self.cache:
            response, timestamp = self.cache[key]
            self.hits += 1
            logger.debug(f"✓ Cache hit (total: {self.hits})")
            return response
        
        self.misses += 1
        return None
    
    def put(self, prompt: str, response: str):
        """Store response in cache"""
        
        key = self._hash_prompt(prompt)
        
        # Simple eviction: remove oldest when full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache, key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
            logger.debug("Cache evicted oldest entry")
        
        import time
        self.cache[key] = (response, time.time())
    
    @staticmethod
    def _hash_prompt(prompt: str) -> str:
        """Hash prompt for cache key"""
        import hashlib
        return hashlib.sha256(prompt.encode()).hexdigest()[:16]
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1%}",
        }
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        logger.info("✓ Cache cleared")


class QueryOptimizer:
    """Optimize database queries"""
    
    def __init__(self):
        self.slow_queries: list = []
        self.slow_threshold_ms = 100
    
    def log_query(self, query: str, execution_time_ms: float):
        """Log query performance"""
        
        if execution_time_ms > self.slow_threshold_ms:
            self.slow_queries.append({
                "query": query[:100],
                "time_ms": execution_time_ms,
                "timestamp": datetime.now().isoformat(),
            })
            logger.warning(f"⚠️ Slow query: {execution_time_ms:.0f}ms - {query[:50]}")
    
    def get_slowest_queries(self, limit: int = 10) -> list:
        """Get slowest queries"""
        return sorted(
            self.slow_queries,
            key=lambda q: q["time_ms"],
            reverse=True
        )[:limit]


class PerformanceOptimizer:
    """Main performance optimization system"""
    
    def __init__(self):
        self.system_monitor = SystemMonitor()
        self.cache = LLMResponseCache()
        self.query_optimizer = QueryOptimizer()
    
    def get_optimization_recommendations(self) -> Dict:
        """Get recommendations for optimization"""
        
        health = self.system_monitor.get_health_status()
        cache_stats = self.cache.get_stats()
        slow_queries = self.query_optimizer.get_slowest_queries()
        
        recommendations = []
        
        # Cache recommendations
        if cache_stats["hit_rate"] < "0.1%":
            recommendations.append({
                "category": "Cache",
                "issue": "Low hit rate",
                "recommendation": "Cache is not effective - check if prompts vary too much",
                "priority": "low",
            })
        
        # Query recommendations
        if slow_queries:
            recommendations.append({
                "category": "Database",
                "issue": f"{len(slow_queries)} slow queries detected",
                "recommendation": "Add database indexes or optimize queries",
                "priority": "medium",
                "examples": slow_queries[:3],
            })
        
        # System recommendations
        if health["alerts"]:
            for alert in health["alerts"]:
                recommendations.append({
                    "category": "System",
                    "issue": alert,
                    "recommendation": "Free up resources or optimize workload",
                    "priority": "high",
                })
        
        return {
            "system_health": health["status"],
            "recommendations": recommendations,
            "cache_stats": cache_stats,
        }


__all__ = [
    "SystemMonitor",
    "LLMResponseCache",
    "QueryOptimizer",
    "PerformanceOptimizer",
]
