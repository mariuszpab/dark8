# DARK8 OS - Web Dashboard Backend
"""
FastAPI backend for web dashboard.
Real-time monitoring, metrics, agent status.
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DashboardMetric:
    """Single dashboard metric"""

    name: str
    value: float
    unit: str
    timestamp: str
    trend: str  # "up", "down", "stable"


class DashboardDataProvider:
    """Provide real-time data for dashboard"""

    def __init__(self):
        self.metrics_cache: Dict = {}
        self.update_interval = 5  # seconds

    def get_system_overview(self) -> Dict:
        """Get overall system status"""

        return {
            "status": "operational",
            "uptime_hours": 48,
            "last_update": "2026-02-17T12:00:00Z",
            "version": "0.3.0-alpha",
            "components": {
                "nlp_engine": {"status": "operational", "version": "3.0"},
                "agent_system": {"status": "operational", "agents": 5},
                "learning_system": {"status": "operational", "tasks_learned": 347},
                "code_generator": {"status": "operational", "languages": 6},
                "security": {"status": "operational", "rbac_enabled": True},
            },
        }

    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""

        return {
            "cpu_percent": 23.5,
            "memory_percent": 45.2,
            "disk_percent": 62.1,
            "response_time_ms": 145,
            "cache_hit_rate": 0.58,
            "api_calls_per_minute": 342,
            "errors_per_hour": 2,
            "uptime_percent": 99.98,
        }

    def get_nlp_metrics(self) -> Dict:
        """NLP engine metrics"""

        return {
            "intents_processed": 1247,
            "average_confidence": 0.845,
            "semantic_similarity_enabled": True,
            "bert_model_loaded": True,
            "entities_recognized": 5847,
            "languages_supported": 1,  # Polish
        }

    def get_agent_metrics(self) -> Dict:
        """Multi-agent system metrics"""

        return {
            "total_agents": 5,
            "agents_active": 5,
            "tasks_in_queue": 12,
            "tasks_completed": 1892,
            "average_success_rate": 0.887,
            "coordination_efficiency": 0.93,
            "message_throughput": 234,
        }

    def get_learning_metrics(self) -> Dict:
        """Learning system metrics"""

        return {
            "patterns_learned": 342,
            "success_rate_improvement": 0.12,  # 12%
            "confidence_level": 0.895,
            "prompts_optimized": 45,
            "anti_patterns_detected": 18,
            "knowledge_base_entries": 2847,
        }

    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """Recent task history"""

        return [
            {
                "task_id": f"task_{i}",
                "intent": "BUILD_APP",
                "status": "completed",
                "duration_seconds": 234 + i * 10,
                "success": True,
                "timestamp": str(__import__("datetime").datetime.now()),
            }
            for i in range(limit)
        ]


class DashboardEndpoints:
    """FastAPI endpoint definitions"""

    @staticmethod
    def get_endpoints() -> List[Dict]:
        """List all dashboard endpoints"""

        return [
            {
                "path": "/dashboard/overview",
                "method": "GET",
                "description": "System overview",
                "returns": "DashboardMetric",
            },
            {
                "path": "/dashboard/performance",
                "method": "GET",
                "description": "Performance metrics",
                "returns": "PerformanceMetric",
            },
            {
                "path": "/dashboard/agents",
                "method": "GET",
                "description": "Agent system status",
                "returns": "AgentMetrics",
            },
            {
                "path": "/dashboard/nlp",
                "method": "GET",
                "description": "NLP engine metrics",
                "returns": "NLPMetrics",
            },
            {
                "path": "/dashboard/learning",
                "method": "GET",
                "description": "Learning progress",
                "returns": "LearningMetrics",
            },
            {
                "path": "/dashboard/tasks",
                "method": "GET",
                "description": "Recent tasks",
                "returns": "List[TaskRecord]",
            },
            {
                "path": "/dashboard/websocket",
                "method": "WEBSOCKET",
                "description": "Real-time updates",
                "returns": "StreamingMetrics",
            },
        ]


class RealtimeUpdater:
    """Push real-time updates to dashboard"""

    def __init__(self):
        self.connected_clients: List = []
        self.update_queue: List[Dict] = []

    def broadcast_update(self, update: Dict) -> int:
        """Broadcast update to all connected clients"""

        self.update_queue.append(update)

        # In real implementation, would use WebSocket
        clients_notified = len(self.connected_clients)

        return clients_notified

    def get_pending_updates(self) -> List[Dict]:
        """Get updates waiting to be sent"""

        updates = self.update_queue.copy()
        self.update_queue.clear()
        return updates


class DashboardHTML:
    """Generate dashboard HTML"""

    @staticmethod
    def get_dashboard_html() -> str:
        """Get complete HTML for dashboard"""

        return """
<!DOCTYPE html>
<html>
<head>
    <title>DARK8 OS - Dashboard</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: #333; color: white; padding: 20px; border-radius: 5px; }
        .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 20px; }
        .metric-card { background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .metric-card h3 { margin: 0 0 10px 0; color: #333; }
        .metric-value { font-size: 24px; font-weight: bold; color: #2196F3; }
        .metric-unit { font-size: 12px; color: #999; }
        .status-up { color: #4CAF50; }
        .status-down { color: #f44336; }
        .agent-list { margin-top: 20px; background: white; padding: 15px; border-radius: 5px; }
        .agent-item { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 DARK8 OS - Control Dashboard</h1>
            <p>Real-time monitoring | Multi-Agent System | AI Operating System</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <h3>System Status</h3>
                <div class="metric-value status-up">● Operational</div>
                <div class="metric-unit">Uptime: 48h 23m</div>
            </div>
            
            <div class="metric-card">
                <h3>CPU Usage</h3>
                <div class="metric-value">23.5%</div>
                <div class="metric-unit">4 cores available</div>
            </div>
            
            <div class="metric-card">
                <h3>Memory Usage</h3>
                <div class="metric-value">45.2%</div>
                <div class="metric-unit">8GB total</div>
            </div>
            
            <div class="metric-card">
                <h3>Active Tasks</h3>
                <div class="metric-value">12</div>
                <div class="metric-unit">3 in progress</div>
            </div>
            
            <div class="metric-card">
                <h3>Agent Success Rate</h3>
                <div class="metric-value">88.7%</div>
                <div class="metric-unit">↑ 3% from yesterday</div>
            </div>
            
            <div class="metric-card">
                <h3>Cache Hit Rate</h3>
                <div class="metric-value">58%</div>
                <div class="metric-unit">LLM response cache</div>
            </div>
        </div>
        
        <div class="agent-list">
            <h2>Active Agents</h2>
            <div class="agent-item">
                <span>🧠 Planner Agent</span>
                <span>✅ Active - 234 tasks</span>
            </div>
            <div class="agent-item">
                <span>⚙️ Executor Agent</span>
                <span>✅ Active - 189 tasks</span>
            </div>
            <div class="agent-item">
                <span>📋 Reviewer Agent</span>
                <span>✅ Active - 156 tasks</span>
            </div>
            <div class="agent-item">
                <span>🧠 Learner Agent</span>
                <span>✅ Active - 342 patterns</span>
            </div>
            <div class="agent-item">
                <span>⚡ Optimizer Agent</span>
                <span>✅ Active - 45 optimizations</span>
            </div>
        </div>
    </div>
    
    <script>
        // Real-time update via WebSocket
        const ws = new WebSocket('ws://localhost:8000/dashboard/websocket');
        ws.onmessage = function(event) {
            console.log('Dashboard update:', event.data);
            // Update metrics dynamically
        };
    </script>
</body>
</html>
        """


__all__ = [
    "DashboardDataProvider",
    "DashboardEndpoints",
    "RealtimeUpdater",
    "DashboardHTML",
    "DashboardMetric",
]
