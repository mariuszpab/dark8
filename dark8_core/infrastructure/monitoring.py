"""
DARK8 OS - Phase 4: Monitoring Stack
System monitorowania metryk, alertów i wizualizacji
Autor: DARK8 Development Team
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque


class MetricType(Enum):
    """Typy metryk"""
    COUNTER = "counter"        # Numerator rosnący
    GAUGE = "gauge"            # Wartość bieżąca
    HISTOGRAM = "histogram"    # Rozkład wartości
    SUMMARY = "summary"        # Podsumowanie


class AlertSeverity(Enum):
    """Priorytet alertu"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Metric:
    """Reprezentacja metryki"""
    name: str
    type: MetricType
    value: float
    labels: Dict[str, str]  # etykiety: {'instance': 'server-1', 'job': 'api'}
    timestamp: datetime = None
    unit: str = ""  # np. "ms", "bytes", "%"
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> dict:
        """Konwersja do słownika"""
        d = asdict(self)
        d['type'] = self.type.value
        d['timestamp'] = self.timestamp.isoformat()
        return d


@dataclass
class Alert:
    """Reprezentacja alertu"""
    alert_id: str
    name: str
    severity: AlertSeverity
    message: str
    metric_name: str
    threshold: float
    current_value: float
    created_at: datetime
    resolved_at: Optional[datetime] = None
    is_active: bool = True


class MetricsCollector:
    """Kolektor metryk (Prometheus-like)"""
    
    def __init__(self, retention_size: int = 100000):
        """
        Inicjalizacja Metrics Collector'a
        
        Args:
            retention_size: Maksymalna liczba metryk w pamięci
        """
        self.metrics: deque = deque(maxlen=retention_size)
        self.metric_registry: Dict[str, List[Metric]] = defaultdict(list)
        self.created_at = datetime.now()
        
    def record_metric(self, metric: Metric) -> None:
        """Rejestracja metryki"""
        self.metrics.append(metric)
        self.metric_registry[metric.name].append(metric)
        
        # Cleanup starych metryk (przechowuj ostatnie 1000 na metrykę)
        if len(self.metric_registry[metric.name]) > 1000:
            self.metric_registry[metric.name] = self.metric_registry[metric.name][-1000:]
    
    def query_metric(self, metric_name: str) -> List[Metric]:
        """Zapytanie do metryki"""
        return self.metric_registry.get(metric_name, [])
    
    def query_range(self, 
                   metric_name: str,
                   start_time: datetime,
                   end_time: datetime) -> List[Metric]:
        """Zapytanie metryk w zakresie czasu"""
        metrics = self.metric_registry.get(metric_name, [])
        return [m for m in metrics if start_time <= m.timestamp <= end_time]
    
    def query_by_labels(self, metric_name: str, labels: Dict[str, str]) -> List[Metric]:
        """Zapytanie metryk po etykietach"""
        metrics = self.metric_registry.get(metric_name, [])
        
        result = []
        for metric in metrics:
            if all(metric.labels.get(k) == v for k, v in labels.items()):
                result.append(metric)
        
        return result
    
    def get_metrics_summary(self) -> Dict:
        """Pobranie podsumowania metryk"""
        return {
            'total_metrics_collected': len(self.metrics),
            'unique_metric_names': len(self.metric_registry),
            'uptime_seconds': (datetime.now() - self.created_at).total_seconds(),
            'retention_size': self.metrics.maxlen
        }


class AlertManager:
    """Manager alertów"""
    
    def __init__(self):
        """Inicjalizacja Alert Manager'a"""
        self.alerts: Dict[str, Alert] = {}
        self.alert_rules: Dict[str, Dict] = {}
        self.alert_history: deque = deque(maxlen=10000)
        self.silenced_alerts: Dict[str, datetime] = {}
        
    def add_alert_rule(self,
                      rule_name: str,
                      metric_name: str,
                      threshold: float,
                      comparison: str = "greater",  # 'greater', 'less', 'equal'
                      severity: AlertSeverity = AlertSeverity.WARNING,
                      for_duration_seconds: int = 300) -> bool:
        """
        Dodanie reguły alertu
        
        Args:
            rule_name: Nazwa reguły
            metric_name: Nazwa metryki do monitorowania
            threshold: Próg alertu
            comparison: Operator porównania
            severity: Priorytet alertu
            for_duration_seconds: Czas przed wysłaniem alertu
            
        Returns:
            bool: Czy reguła została dodana
        """
        self.alert_rules[rule_name] = {
            'metric_name': metric_name,
            'threshold': threshold,
            'comparison': comparison,
            'severity': severity,
            'duration': for_duration_seconds,
            'created_at': datetime.now().isoformat()
        }
        return True
    
    def evaluate_alerts(self, metrics_collector: MetricsCollector) -> List[Alert]:
        """
        Ocena alertów na podstawie metryk
        
        Args:
            metrics_collector: Kolektor metryk
            
        Returns:
            List[Alert]: Nowe aktywne alerty
        """
        new_alerts = []
        
        for rule_name, rule in self.alert_rules.items():
            metric_name = rule['metric_name']
            metrics = metrics_collector.query_metric(metric_name)
            
            if not metrics:
                continue
            
            # Pobierz ostatnią metrykę
            latest_metric = metrics[-1]
            threshold = rule['threshold']
            comparison = rule['comparison']
            
            # Porównanie
            should_trigger = False
            
            if comparison == 'greater' and latest_metric.value > threshold:
                should_trigger = True
            elif comparison == 'less' and latest_metric.value < threshold:
                should_trigger = True
            elif comparison == 'equal' and latest_metric.value == threshold:
                should_trigger = True
            
            if should_trigger:
                # Sprawdzenie czy alert jest już aktywny
                alert_key = f"{rule_name}-{metric_name}"
                
                if alert_key not in self.alerts:
                    # Nowy alert
                    alert = Alert(
                        alert_id=alert_key,
                        name=rule_name,
                        severity=rule['severity'],
                        message=f"Metric {metric_name} = {latest_metric.value} (threshold: {threshold})",
                        metric_name=metric_name,
                        threshold=threshold,
                        current_value=latest_metric.value,
                        created_at=datetime.now()
                    )
                    
                    self.alerts[alert_key] = alert
                    new_alerts.append(alert)
                    
                    # Zapis do historii
                    self.alert_history.append({
                        'alert_id': alert_key,
                        'name': rule_name,
                        'action': 'triggered',
                        'timestamp': datetime.now().isoformat()
                    })
        
        return new_alerts
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Rozwiązanie alertu"""
        if alert_id in self.alerts:
            alert = self.alerts[alert_id]
            alert.is_active = False
            alert.resolved_at = datetime.now()
            
            self.alert_history.append({
                'alert_id': alert_id,
                'name': alert.name,
                'action': 'resolved',
                'timestamp': datetime.now().isoformat()
            })
            
            return True
        return False
    
    def silence_alert(self, alert_id: str, duration_minutes: int = 30) -> bool:
        """Wyciszenie alertu"""
        if alert_id in self.alerts:
            silence_until = datetime.now() + timedelta(minutes=duration_minutes)
            self.silenced_alerts[alert_id] = silence_until
            return True
        return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Pobranie aktywnych alertów"""
        now = datetime.now()
        active = []
        
        for alert_id, alert in self.alerts.items():
            if alert.is_active:
                # Sprawdzenie czy alert nie jest wyciszony
                if alert_id in self.silenced_alerts:
                    if now < self.silenced_alerts[alert_id]:
                        continue  # Alert jest wyciszony
                    else:
                        del self.silenced_alerts[alert_id]
                
                active.append(alert)
        
        return active
    
    def get_alert_stats(self) -> Dict:
        """Statystyki alertów"""
        active = self.get_active_alerts()
        silenced = len(self.silenced_alerts)
        
        return {
            'total_alerts': len(self.alerts),
            'active_alerts': len(active),
            'silenced_alerts': silenced,
            'critical_alerts': sum(1 for a in active if a.severity == AlertSeverity.CRITICAL),
            'warning_alerts': sum(1 for a in active if a.severity == AlertSeverity.WARNING),
            'alert_history_entries': len(self.alert_history)
        }


class Dashboard:
    """Dashboard do wizualizacji metryk"""
    
    def __init__(self, metrics_collector: MetricsCollector, alert_manager: AlertManager):
        """Inicjalizacja Dashboard'u"""
        self.metrics_collector = metrics_collector
        self.alert_manager = alert_manager
        self.dashboards: Dict[str, Dict] = {}
        self.created_at = datetime.now()
        
    def create_dashboard(self, name: str, description: str = "") -> bool:
        """Tworzenie dashboarda"""
        self.dashboards[name] = {
            'name': name,
            'description': description,
            'widgets': [],
            'created_at': datetime.now().isoformat()
        }
        return True
    
    def add_widget(self,
                  dashboard_name: str,
                  widget_name: str,
                  metric_name: str,
                  widget_type: str = "graph") -> bool:
        """
        Dodanie widgetu do dashboardu
        
        Args:
            dashboard_name: Nazwa dashboardu
            widget_name: Nazwa widgetu
            metric_name: Nazwa metryki
            widget_type: Typ widgetu ('graph', 'gauge', 'table')
            
        Returns:
            bool: Czy widget został dodany
        """
        if dashboard_name not in self.dashboards:
            return False
        
        widget = {
            'name': widget_name,
            'type': widget_type,
            'metric_name': metric_name,
            'created_at': datetime.now().isoformat()
        }
        
        self.dashboards[dashboard_name]['widgets'].append(widget)
        return True
    
    def get_dashboard_data(self, dashboard_name: str) -> Dict:
        """Pobranie danych dashboardu"""
        if dashboard_name not in self.dashboards:
            return {}
        
        dashboard = self.dashboards[dashboard_name]
        data = {
            'name': dashboard['name'],
            'created_at': dashboard['created_at'],
            'widgets': []
        }
        
        for widget in dashboard['widgets']:
            metric_name = widget['metric_name']
            metrics = self.metrics_collector.query_metric(metric_name)
            
            if metrics:
                latest = metrics[-1]
                data['widgets'].append({
                    'name': widget['name'],
                    'type': widget['type'],
                    'metric_name': metric_name,
                    'value': latest.value,
                    'unit': latest.unit,
                    'timestamp': latest.timestamp.isoformat()
                })
        
        return data
    
    def get_system_overview(self) -> Dict:
        """Pobranie overview'u systemu"""
        metrics_summary = self.metrics_collector.get_metrics_summary()
        alerts_summary = self.alert_manager.get_alert_stats()
        active_alerts = self.alert_manager.get_active_alerts()
        
        return {
            'metrics': metrics_summary,
            'alerts': alerts_summary,
            'active_alerts': [
                {
                    'id': a.alert_id,
                    'name': a.name,
                    'severity': a.severity.value,
                    'message': a.message,
                    'created_at': a.created_at.isoformat()
                }
                for a in active_alerts
            ],
            'uptime_seconds': (datetime.now() - self.created_at).total_seconds()
        }


class Logger:
    """Logger dla metryki usług"""
    
    def __init__(self, max_logs: int = 10000):
        """Inicjalizacja Logger'a"""
        self.logs: deque = deque(maxlen=max_logs)
        self.log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        
    def log(self, level: str, component: str, message: str) -> None:
        """Zapisanie logu"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'component': component,
            'message': message
        }
        self.logs.append(log_entry)
    
    def query_logs(self, 
                   level: Optional[str] = None,
                   component: Optional[str] = None,
                   limit: int = 100) -> List[Dict]:
        """Zapytanie do logów"""
        result = list(self.logs)
        
        if level:
            result = [entry for entry in result if entry['level'] == level]
        
        if component:
            result = [entry for entry in result if entry['component'] == component]
        
        return result[-limit:]
    
    def get_log_stats(self) -> Dict:
        """Statystyki logów"""
        stats = {'total_logs': len(self.logs)}
        
        for level in self.log_levels:
            count = sum(1 for entry in self.logs if entry['level'] == level)
            stats[f'{level.lower()}_count'] = count
        
        return stats


def test_monitoring_stack():
    """Test Monitoring Stack"""
    print("\n🔧 Testowanie Monitoring Stack...")
    
    # Inicjalizacja
    collector = MetricsCollector()
    alert_manager = AlertManager()
    dashboard = Dashboard(collector, alert_manager)
    logger = Logger()
    
    print("✅ Monitoring Stack inicjalizowany")
    
    # Rejestracja metryk
    for i in range(10):
        metric = Metric(
            name='http_requests_total',
            type=MetricType.COUNTER,
            value=float(i * 100),
            labels={'job': 'api', 'instance': 'server-1'},
            unit='requests'
        )
        collector.record_metric(metric)
    
    print(f"✅ Metryki zarejestrowane: {len(collector.metrics)}")
    
    # Reguły alertów
    alert_manager.add_alert_rule(
        'high_request_rate',
        'http_requests_total',
        threshold=500,
        comparison='greater',
        severity=AlertSeverity.WARNING
    )
    
    print("✅ Reguły alertów dodane")
    
    # Ocena alertów
    alerts = alert_manager.evaluate_alerts(collector)
    print(f"✅ Alerty: {len(alerts)}")
    
    # Dashboard
    dashboard.create_dashboard('Main', 'Główny dashboard')
    dashboard.add_widget('Main', 'Requests', 'http_requests_total', 'graph')
    
    overview = dashboard.get_system_overview()
    print(f"✅ Dashboard overview: {json.dumps(overview, indent=2)}")
    
    # Logging
    logger.log('INFO', 'system', 'Monitoring started')
    logger.log('WARNING', 'api', 'High CPU usage detected')
    
    log_stats = logger.get_log_stats()
    print(f"✅ Log stats: {log_stats}")


if __name__ == '__main__':
    test_monitoring_stack()
