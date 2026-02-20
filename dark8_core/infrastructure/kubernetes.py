"""
DARK8 OS - Phase 4: Kubernetes Manager
Zarządzanie orkiestracją kontenerów i skalowaniem
Autor: DARK8 Development Team
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class PodStatus(Enum):
    """Status podu w klastrze Kubernetes"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class Pod:
    """Reprezentacja podu Kubernetes"""
    name: str
    namespace: str
    image: str
    status: PodStatus
    replicas: int
    ready_replicas: int
    created_at: datetime
    restart_count: int = 0
    cpu_limit: str = "500m"  # millicores
    memory_limit: str = "512Mi"
    
    def is_healthy(self) -> bool:
        """Sprawdzenie czy pod jest zdolny"""
        return (self.status == PodStatus.RUNNING and 
                self.ready_replicas == self.replicas)
    
    def to_dict(self) -> dict:
        """Konwersja do słownika"""
        d = asdict(self)
        d['status'] = self.status.value
        d['created_at'] = self.created_at.isoformat()
        return d


@dataclass
class Service:
    """Reprezentacja serwisu Kubernetes"""
    name: str
    namespace: str
    service_type: str  # ClusterIP, NodePort, LoadBalancer
    cluster_ip: str
    external_ip: Optional[str]
    port: int
    target_port: int
    created_at: datetime


class KubernetesCluster:
    """Manager orkiestracji Kubernetes dla DARK8 OS"""
    
    def __init__(self, config: Dict = None):
        """Inicjalizacja klastera K8s"""
        self.config = config or {}
        self.cluster_context = self.config.get('context', 'dark8-prod')
        self.namespace = self.config.get('namespace', 'dark8-system')
        self.pods: Dict[str, Pod] = {}
        self.services: Dict[str, Service] = {}
        self.deployments: Dict[str, dict] = {}
        self.cluster_created_at = datetime.now()
        self.version = "1.28.0"  # K8s version
        self.nodes = 3  # Default number of nodes
        
    def create_deployment(self, 
                         name: str,
                         image: str,
                         replicas: int = 3,
                         cpu: str = "250m",
                         memory: str = "256Mi") -> bool:
        """
        Tworzenie deployment w klastrze
        
        Args:
            name: Nazwa deploymentu
            image: Docker image URI
            replicas: Liczba replik
            cpu: Limit CPU
            memory: Limit pamięci
            
        Returns:
            bool: Czy deployment został utworzony pomyślnie
        """
        try:
            deployment = {
                'name': name,
                'image': image,
                'replicas': replicas,
                'cpu_limit': cpu,
                'memory_limit': memory,
                'created_at': datetime.now().isoformat(),
                'status': 'creating',
                'ready_replicas': 0,
                'update_strategy': 'RollingUpdate'
            }
            
            # Symulacja tworzenia podów
            for i in range(replicas):
                pod_name = f"{name}-pod-{i}"
                self.pods[pod_name] = Pod(
                    name=pod_name,
                    namespace=self.namespace,
                    image=image,
                    status=PodStatus.PENDING,
                    replicas=replicas,
                    ready_replicas=0,
                    created_at=datetime.now(),
                    cpu_limit=cpu,
                    memory_limit=memory
                )
            
            self.deployments[name] = deployment
            
            # Simulacja time do ready
            time.sleep(0.1)
            for pod_name in self.pods:
                if pod_name.startswith(name):
                    self.pods[pod_name].status = PodStatus.RUNNING
                    self.pods[pod_name].ready_replicas = replicas
            
            deployment['status'] = 'running'
            deployment['ready_replicas'] = replicas
            
            return True
            
        except Exception as e:
            print(f"❌ Błąd tworzenia deployment: {e}")
            return False
    
    def scale_deployment(self, name: str, new_replicas: int) -> bool:
        """
        Skalowanie deployment do nowej liczby replik
        
        Args:
            name: Nazwa deploymentu
            new_replicas: Nowa liczba replik
            
        Returns:
            bool: Czy skalowanie powiodło się
        """
        if name not in self.deployments:
            return False
        
        old_replicas = self.deployments[name]['replicas']
        self.deployments[name]['replicas'] = new_replicas
        
        # Symulacja skalowania
        if new_replicas > old_replicas:
            # Scale up
            for i in range(old_replicas, new_replicas):
                pod_name = f"{name}-pod-{i}"
                self.pods[pod_name] = Pod(
                    name=pod_name,
                    namespace=self.namespace,
                    image=self.deployments[name]['image'],
                    status=PodStatus.RUNNING,
                    replicas=new_replicas,
                    ready_replicas=new_replicas,
                    created_at=datetime.now()
                )
        elif new_replicas < old_replicas:
            # Scale down
            for i in range(new_replicas, old_replicas):
                pod_name = f"{name}-pod-{i}"
                if pod_name in self.pods:
                    del self.pods[pod_name]
        
        self.deployments[name]['ready_replicas'] = new_replicas
        return True
    
    def get_pod_status(self, pod_name: str) -> Optional[Pod]:
        """Pobranie statusu podu"""
        return self.pods.get(pod_name)
    
    def get_deployment_status(self, name: str) -> Optional[Dict]:
        """Pobranie statusu deploymentu"""
        return self.deployments.get(name)
    
    def create_service(self,
                      name: str,
                      selector: Dict,
                      port: int,
                      target_port: int,
                      service_type: str = "ClusterIP") -> bool:
        """Tworzenie serwisu Kubernetes"""
        try:
            service = Service(
                name=name,
                namespace=self.namespace,
                service_type=service_type,
                cluster_ip=f"10.0.0.{len(self.services) + 1}",
                external_ip=None if service_type == "ClusterIP" else "1.2.3.4",
                port=port,
                target_port=target_port,
                created_at=datetime.now()
            )
            
            self.services[name] = service
            return True
            
        except Exception as e:
            print(f"❌ Błąd tworzenia service: {e}")
            return False
    
    def get_logs(self, pod_name: str, lines: int = 100) -> str:
        """Pobranie logów z podu"""
        if pod_name not in self.pods:
            return "Pod not found"
        
        pod = self.pods[pod_name]
        logs = f"""
[{pod.created_at.isoformat()}] Pod {pod_name} logs:
- Status: {pod.status.value}
- Image: {pod.image}
- CPU Limit: {pod.cpu_limit}
- Memory Limit: {pod.memory_limit}
- Restarts: {pod.restart_count}
[INFO] Container started successfully
[INFO] Service health check passed
[INFO] Ready to accept connections
"""
        return logs
    
    def list_pods(self, namespace: Optional[str] = None) -> List[Pod]:
        """Wylistowanie wszystkich podów"""
        ns = namespace or self.namespace
        return [pod for pod in self.pods.values() if pod.namespace == ns]
    
    def list_services(self) -> List[Service]:
        """Wylistowanie wszystkich serwisów"""
        return list(self.services.values())
    
    def delete_deployment(self, name: str) -> bool:
        """Usunięcie deploymentu i jego podów"""
        if name not in self.deployments:
            return False
        
        # Usuwanie podów
        pods_to_delete = [p for p in self.pods if p.startswith(name)]
        for pod in pods_to_delete:
            del self.pods[pod]
        
        del self.deployments[name]
        return True
    
    def get_cluster_info(self) -> Dict:
        """Pobranie informacji o klastrze"""
        return {
            'context': self.cluster_context,
            'namespace': self.namespace,
            'version': self.version,
            'nodes': self.nodes,
            'created_at': self.cluster_created_at.isoformat(),
            'total_pods': len(self.pods),
            'total_services': len(self.services),
            'total_deployments': len(self.deployments),
            'healthy_pods': sum(1 for p in self.pods.values() if p.is_healthy())
        }


class DeploymentManager:
    """Menedżer deploymentów z automatyzacją"""
    
    def __init__(self, cluster: KubernetesCluster):
        """Inicjalizacja managera deploymentów"""
        self.cluster = cluster
        self.deployment_history: List[Dict] = []
        self.rollback_points: Dict[str, List[Dict]] = {}
        
    def deploy_service(self,
                      name: str,
                      image: str,
                      replicas: int = 3,
                      wait_for_ready: bool = True) -> bool:
        """Deployment serwisu z czekaniem na gotowość"""
        success = self.cluster.create_deployment(
            name=name,
            image=image,
            replicas=replicas
        )
        
        if success:
            self.deployment_history.append({
                'name': name,
                'image': image,
                'replicas': replicas,
                'timestamp': datetime.now().isoformat(),
                'status': 'deployed'
            })
            
            # Inicjalizacja historia rollback'u
            if name not in self.rollback_points:
                self.rollback_points[name] = []
            
            self.rollback_points[name].append({
                'image': image,
                'replicas': replicas,
                'timestamp': datetime.now().isoformat()
            })
        
        return success
    
    def rolling_update(self, name: str, new_image: str) -> bool:
        """
        Rolling Update - aktualizacja bez downtime'u
        
        Args:
            name: Nazwa deploymentu
            new_image: Nowy Docker image
            
        Returns:
            bool: Czy update powiódł się
        """
        deployment = self.cluster.get_deployment_status(name)
        if not deployment:
            return False
        
        # Updateowanie deployment
        deployment['image'] = new_image
        deployment['status'] = 'updating'
        
        # Symulacja rolling update (stop 1 pod, update, start nowy)
        # W rzeczywistym K8s to jest automatyczne
        time.sleep(0.05)
        
        deployment['status'] = 'running'
        
        # Zapis do historii
        self.deployment_history.append({
            'name': name,
            'action': 'rolling_update',
            'new_image': new_image,
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        })
        
        return True
    
    def rollback_deployment(self, name: str) -> bool:
        """Rollback deploymentu do poprzedniej wersji"""
        if name not in self.rollback_points or not self.rollback_points[name]:
            return False
        
        # Pobierz poprzednią wersję
        previous = self.rollback_points[name][-2] if len(self.rollback_points[name]) > 1 else self.rollback_points[name][-1]
        
        return self.rolling_update(name, previous['image'])


class ResourceScaler:
    """Autoskalowanie zasobów na podstawie metryk"""
    
    def __init__(self, cluster: KubernetesCluster):
        """Inicjalizacja scalera"""
        self.cluster = cluster
        self.scaling_policies: Dict[str, Dict] = {}
        self.last_scaled: Dict[str, datetime] = {}
        
    def add_scaling_policy(self,
                          deployment_name: str,
                          min_replicas: int = 2,
                          max_replicas: int = 10,
                          cpu_threshold: float = 80.0,
                          memory_threshold: float = 80.0,
                          cooldown_seconds: int = 60) -> bool:
        """Dodanie polityki autoskalowania"""
        self.scaling_policies[deployment_name] = {
            'min_replicas': min_replicas,
            'max_replicas': max_replicas,
            'cpu_threshold': cpu_threshold,
            'memory_threshold': memory_threshold,
            'cooldown_seconds': cooldown_seconds,
            'created_at': datetime.now().isoformat()
        }
        return True
    
    def evaluate_scaling(self, deployment_name: str, current_metrics: Dict) -> Optional[int]:
        """
        Ocena czy skalowanie jest potrzebne
        
        Args:
            deployment_name: Nazwa deploymentu
            current_metrics: Bieżące metryki (cpu, memory)
            
        Returns:
            Optional[int]: Nowa liczba replik lub None
        """
        if deployment_name not in self.scaling_policies:
            return None
        
        policy = self.scaling_policies[deployment_name]
        deployment = self.cluster.get_deployment_status(deployment_name)
        
        if not deployment:
            return None
        
        # Sprawdzenie cooldown'u
        last_scaled = self.last_scaled.get(deployment_name, datetime.now() - timedelta(minutes=5))
        if (datetime.now() - last_scaled).seconds < policy['cooldown_seconds']:
            return None
        
        current_replicas = deployment['replicas']
        cpu_usage = current_metrics.get('cpu', 0)
        memory_usage = current_metrics.get('memory', 0)
        
        # Decyzja skalowania
        if cpu_usage > policy['cpu_threshold'] or memory_usage > policy['memory_threshold']:
            # Scale up
            new_replicas = min(current_replicas + 1, policy['max_replicas'])
        elif cpu_usage < policy['cpu_threshold'] * 0.5 and memory_usage < policy['memory_threshold'] * 0.5:
            # Scale down
            new_replicas = max(current_replicas - 1, policy['min_replicas'])
        else:
            return None
        
        if new_replicas != current_replicas:
            self.cluster.scale_deployment(deployment_name, new_replicas)
            self.last_scaled[deployment_name] = datetime.now()
            return new_replicas
        
        return None
    
    def get_scaling_recommendations(self) -> List[Dict]:
        """Pobranie rekomendacji skalowania"""
        recommendations = []
        
        for deployment_name, policy in self.scaling_policies.items():
            deployment = self.cluster.get_deployment_status(deployment_name)
            if deployment:
                recommendations.append({
                    'deployment': deployment_name,
                    'current_replicas': deployment['replicas'],
                    'min_replicas': policy['min_replicas'],
                    'max_replicas': policy['max_replicas'],
                    'cpu_threshold': policy['cpu_threshold'],
                    'memory_threshold': policy['memory_threshold']
                })
        
        return recommendations


class HealthChecker:
    """Checker zdrowia podów i serwisów"""
    
    def __init__(self, cluster: KubernetesCluster):
        """Inicjalizacja zdravego checkera"""
        self.cluster = cluster
        self.health_checks: Dict[str, Dict] = {}
        
    def add_health_check(self,
                        pod_name: str,
                        check_type: str = "http",
                        endpoint: str = "/health",
                        interval_seconds: int = 10) -> bool:
        """Dodanie health check'u dla podu"""
        self.health_checks[pod_name] = {
            'type': check_type,
            'endpoint': endpoint,
            'interval': interval_seconds,
            'last_check': datetime.now().isoformat(),
            'status': 'healthy'
        }
        return True
    
    def perform_health_checks(self) -> Dict[str, str]:
        """Wykonanie wszystkich health check'ów"""
        results = {}
        
        for pod_name, check in self.health_checks.items():
            pod = self.cluster.get_pod_status(pod_name)
            
            if not pod:
                results[pod_name] = 'pod_not_found'
            elif pod.status == PodStatus.RUNNING:
                # Symulacja HTTP check
                results[pod_name] = 'healthy'
                check['status'] = 'healthy'
            else:
                results[pod_name] = 'unhealthy'
                check['status'] = 'unhealthy'
            
            check['last_check'] = datetime.now().isoformat()
        
        return results
    
    def get_health_summary(self) -> Dict:
        """Pobranie podsumowania zdrowia"""
        total = len(self.health_checks)
        healthy = sum(1 for c in self.health_checks.values() if c['status'] == 'healthy')
        
        return {
            'total_checks': total,
            'healthy': healthy,
            'unhealthy': total - healthy,
            'health_percentage': (healthy / total * 100) if total > 0 else 0
        }


def test_kubernetes_manager():
    """Test funkcjonalności Kubernetes Manager"""
    print("\n🔧 Testowanie Kubernetes Manager...")
    
    # Inicjalizacja klastera
    cluster = KubernetesCluster({
        'context': 'dark8-prod',
        'namespace': 'dark8-system'
    })
    
    print(f"✅ Klaster zainicjalizowany: {cluster.cluster_context}")
    
    # Deployment serwisów
    cluster.create_deployment('dark8-api', 'dark8/api:v1.0', replicas=3)
    cluster.create_deployment('dark8-worker', 'dark8/worker:v1.0', replicas=2)
    
    print(f"✅ Deployments: {len(cluster.deployments)}")
    print(f"✅ Pody: {len(cluster.pods)}")
    
    # Skalowanie
    cluster.scale_deployment('dark8-api', 5)
    print(f"✅ Scale up: dark8-api -> 5 replik")
    
    # Serwisy
    cluster.create_service('dark8-api', {'app': 'dark8-api'}, 80, 8080, 'LoadBalancer')
    print(f"✅ Serwisy: {len(cluster.services)}")
    
    # Info o klastrze
    info = cluster.get_cluster_info()
    print(f"✅ Klaster info: {json.dumps(info, indent=2, default=str)}")


if __name__ == '__main__':
    test_kubernetes_manager()
