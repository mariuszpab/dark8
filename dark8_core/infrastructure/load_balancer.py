"""
DARK8 OS - Phase 4: Load Balancer
Dystrybucja ruchu i równoważenie obciążenia
Autor: DARK8 Development Team
"""

import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque


class LoadBalancingAlgorithm(Enum):
    """Algorytmy równoważenia obciążenia"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    IP_HASH = "ip_hash"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    RANDOM = "random"
    LATENCY_AWARE = "latency_aware"


@dataclass
class Backend:
    """Reprezentacja backendu (serwer/instancja)"""
    id: str
    host: str
    port: int
    weight: float = 1.0  # Waga dla weighted algorithms
    max_connections: int = 1000
    healthy: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Konwersja do słownika"""
        d = asdict(self)
        d['created_at'] = self.created_at.isoformat()
        return d


@dataclass
class Connection:
    """Reprezentacja połączenia klienta"""
    client_ip: str
    backend_id: str
    established_at: datetime
    bytes_sent: int = 0
    bytes_received: int = 0
    active: bool = True


class LoadBalancer:
    """
    Główny Load Balancer z wieloma algorytmami dystrybucji
    """
    
    def __init__(self, 
                 name: str,
                 algorithm: LoadBalancingAlgorithm = LoadBalancingAlgorithm.ROUND_ROBIN,
                 timeout_seconds: int = 30):
        """
        Inicjalizacja Load Balancera
        
        Args:
            name: Nazwa LB
            algorithm: Algorytm równoważenia
            timeout_seconds: Timeout dla nieaktywnych połączeń
        """
        self.name = name
        self.algorithm = algorithm
        self.timeout_seconds = timeout_seconds
        self.backends: Dict[str, Backend] = {}
        self.connections: List[Connection] = []
        self.round_robin_index = 0
        self.backend_connection_count: Dict[str, int] = defaultdict(int)
        self.backend_latencies: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.session_affinity: Dict[str, str] = {}  # client_ip -> backend_id
        self.created_at = datetime.now()
        
    def add_backend(self, backend: Backend) -> bool:
        """
        Dodanie backendu do LB
        
        Args:
            backend: Backend do dodania
            
        Returns:
            bool: Czy backend został dodany
        """
        try:
            self.backends[backend.id] = backend
            self.backend_connection_count[backend.id] = 0
            return True
        except Exception as e:
            print(f"❌ Błąd dodawania backend: {e}")
            return False
    
    def remove_backend(self, backend_id: str) -> bool:
        """Usunięcie backendu"""
        if backend_id in self.backends:
            del self.backends[backend_id]
            del self.backend_connection_count[backend_id]
            return True
        return False
    
    def select_backend(self, client_ip: str) -> Optional[Backend]:
        """
        Wybór backendu dla klienta
        
        Args:
            client_ip: IP klienta
            
        Returns:
            Backend lub None jeśli brak dostępnych
        """
        healthy_backends = [b for b in self.backends.values() if b.healthy]
        
        if not healthy_backends:
            return None
        
        # Session affinity
        if client_ip in self.session_affinity:
            backend_id = self.session_affinity[client_ip]
            if backend_id in self.backends and self.backends[backend_id].healthy:
                return self.backends[backend_id]
        
        # Selekcja na podstawie algorytmu
        if self.algorithm == LoadBalancingAlgorithm.ROUND_ROBIN:
            backend = self._select_round_robin(healthy_backends)
        
        elif self.algorithm == LoadBalancingAlgorithm.LEAST_CONNECTIONS:
            backend = self._select_least_connections(healthy_backends)
        
        elif self.algorithm == LoadBalancingAlgorithm.IP_HASH:
            backend = self._select_ip_hash(client_ip, healthy_backends)
        
        elif self.algorithm == LoadBalancingAlgorithm.WEIGHTED_ROUND_ROBIN:
            backend = self._select_weighted_round_robin(healthy_backends)
        
        elif self.algorithm == LoadBalancingAlgorithm.LATENCY_AWARE:
            backend = self._select_latency_aware(healthy_backends)
        
        else:
            backend = healthy_backends[0]
        
        # Zapis session affinity
        if backend:
            self.session_affinity[client_ip] = backend.id
        
        return backend
    
    def _select_round_robin(self, backends: List[Backend]) -> Backend:
        """Round Robin - kolejna kolej"""
        backend = backends[self.round_robin_index % len(backends)]
        self.round_robin_index += 1
        return backend
    
    def _select_least_connections(self, backends: List[Backend]) -> Backend:
        """Least Connections - najmniej połączeń"""
        return min(backends, 
                  key=lambda b: self.backend_connection_count[b.id])
    
    def _select_ip_hash(self, client_ip: str, backends: List[Backend]) -> Backend:
        """IP Hash - hasz IP dla consistency"""
        hash_val = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        return backends[hash_val % len(backends)]
    
    def _select_weighted_round_robin(self, backends: List[Backend]) -> Backend:
        """Weighted Round Robin - biorąc pod uwagę wagę"""
        total_weight = sum(b.weight for b in backends)
        choice = (self.round_robin_index % total_weight)
        self.round_robin_index += 1
        
        current = 0
        for backend in backends:
            current += backend.weight
            if choice < current:
                return backend
        
        return backends[0]
    
    def _select_latency_aware(self, backends: List[Backend]) -> Backend:
        """Latency Aware - biorąc pod uwagę latencję"""
        best_backend = backends[0]
        best_score = float('inf')
        
        for backend in backends:
            latencies = self.backend_latencies[backend.id]
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
            else:
                avg_latency = 0
            
            # Score = latency + connection count
            score = avg_latency + (self.backend_connection_count[backend.id] * 0.1)
            
            if score < best_score:
                best_score = score
                best_backend = backend
        
        return best_backend
    
    def handle_request(self, client_ip: str) -> Optional[Tuple[str, int]]:
        """
        Obsłużenie żądania klienta
        
        Args:
            client_ip: IP klienta
            
        Returns:
            Tuple (host, port) lub None
        """
        backend = self.select_backend(client_ip)
        
        if not backend:
            return None
        
        # Utwórz connection
        connection = Connection(
            client_ip=client_ip,
            backend_id=backend.id,
            established_at=datetime.now()
        )
        
        self.connections.append(connection)
        self.backend_connection_count[backend.id] += 1
        
        # Cleanup starych połączeń
        self._cleanup_connections()
        
        return (backend.host, backend.port)
    
    def record_latency(self, backend_id: str, latency_ms: float) -> None:
        """Rejestracja latencji backendu"""
        if backend_id in self.backend_latencies:
            self.backend_latencies[backend_id].append(latency_ms)
    
    def close_connection(self, client_ip: str, bytes_sent: int = 0, bytes_received: int = 0) -> None:
        """Zamknięcie połączenia"""
        for conn in self.connections:
            if conn.client_ip == client_ip and conn.active:
                conn.active = False
                conn.bytes_sent = bytes_sent
                conn.bytes_received = bytes_received
                
                backend_id = conn.backend_id
                self.backend_connection_count[backend_id] -= 1
                break
    
    def _cleanup_connections(self) -> None:
        """Cleanup timeout'owanych połączeń"""
        now = datetime.now()
        timeout_delta = timedelta(seconds=self.timeout_seconds)
        
        for i, conn in enumerate(self.connections):
            if conn.active and (now - conn.established_at) > timeout_delta:
                conn.active = False
                self.backend_connection_count[conn.backend_id] -= 1
        
        # Usuń nieaktywne
        self.connections = [c for c in self.connections if c.active]
    
    def get_stats(self) -> Dict:
        """Pobranie statystyk LB"""
        total_bytes_sent = sum(c.bytes_sent for c in self.connections)
        total_bytes_received = sum(c.bytes_received for c in self.connections)
        
        return {
            'name': self.name,
            'algorithm': self.algorithm.value,
            'total_backends': len(self.backends),
            'healthy_backends': sum(1 for b in self.backends.values() if b.healthy),
            'active_connections': len([c for c in self.connections if c.active]),
            'total_connections': len(self.connections),
            'total_bytes_sent': total_bytes_sent,
            'total_bytes_received': total_bytes_received,
            'uptime_seconds': (datetime.now() - self.created_at).total_seconds()
        }
    
    def get_backend_stats(self) -> List[Dict]:
        """Pobranie statystyk każdego backendu"""
        stats = []
        
        for backend in self.backends.values():
            latencies = self.backend_latencies[backend.id]
            avg_latency = (sum(latencies) / len(latencies)) if latencies else 0
            
            stats.append({
                'backend_id': backend.id,
                'host': backend.host,
                'port': backend.port,
                'healthy': backend.healthy,
                'active_connections': self.backend_connection_count[backend.id],
                'avg_latency_ms': avg_latency,
                'weight': backend.weight
            })
        
        return stats


class HealthMonitor:
    """Monitor zdrowia backendu"""
    
    def __init__(self, lb: LoadBalancer, check_interval_seconds: int = 5):
        """Inicjalizacja Health Monitora"""
        self.lb = lb
        self.check_interval = check_interval_seconds
        self.last_check_time: Dict[str, datetime] = {}
        self.failed_checks: Dict[str, int] = defaultdict(int)
        self.max_failures: int = 3
        
    def perform_health_check(self, backend_id: str) -> bool:
        """
        Przeprowadzenie health check'u backendu
        
        Args:
            backend_id: ID backendu
            
        Returns:
            bool: Czy backend jest zdrowy
        """
        if backend_id not in self.lb.backends:
            return False
        
        backend = self.lb.backends[backend_id]
        
        try:
            # Symulacja health check'u (w rzeczywistości HTTP GET do /health)
            is_healthy = True
            
            if is_healthy:
                backend.healthy = True
                self.failed_checks[backend_id] = 0
            else:
                self.failed_checks[backend_id] += 1
                
                if self.failed_checks[backend_id] >= self.max_failures:
                    backend.healthy = False
            
            self.last_check_time[backend_id] = datetime.now()
            return backend.healthy
            
        except Exception as e:
            self.failed_checks[backend_id] += 1
            
            if self.failed_checks[backend_id] >= self.max_failures:
                backend.healthy = False
            
            return False
    
    def check_all_backends(self) -> Dict[str, bool]:
        """Sprawdzenie wszystkich backendu"""
        results = {}
        
        for backend_id in self.lb.backends.keys():
            results[backend_id] = self.perform_health_check(backend_id)
        
        return results
    
    def get_health_summary(self) -> Dict:
        """Podsumowanie zdrowia"""
        total = len(self.lb.backends)
        healthy = sum(1 for b in self.lb.backends.values() if b.healthy)
        
        return {
            'total_backends': total,
            'healthy_backends': healthy,
            'unhealthy_backends': total - healthy,
            'health_percentage': (healthy / total * 100) if total > 0 else 0
        }


class RateLimiter:
    """Limitowanie rate'u dla backendu"""
    
    def __init__(self, requests_per_minute: int = 1000):
        """
        Inicjalizacja Rate Limitera
        
        Args:
            requests_per_minute: Limit żądań na minutę
        """
        self.requests_per_minute = requests_per_minute
        self.client_requests: Dict[str, deque] = defaultdict(lambda: deque(maxlen=requests_per_minute))
        self.blocked_clients: Dict[str, datetime] = {}
        self.block_duration = 60  # sekundy
        
    def is_allowed(self, client_ip: str) -> bool:
        """
        Sprawdzenie czy żądanie klienta jest dozwolone
        
        Args:
            client_ip: IP klienta
            
        Returns:
            bool: Czy żądanie jest dopuszczalne
        """
        now = datetime.now()
        
        # Sprawdzenie czy klient jest zablokowany
        if client_ip in self.blocked_clients:
            block_end = self.blocked_clients[client_ip]
            if now < block_end:
                return False
            else:
                del self.blocked_clients[client_ip]
        
        # Liczenie żądań w ostatniej minucie
        requests = self.client_requests[client_ip]
        requests.append(now)
        
        one_minute_ago = now - timedelta(minutes=1)
        recent_requests = sum(1 for r in requests if r > one_minute_ago)
        
        if recent_requests > self.requests_per_minute:
            self.blocked_clients[client_ip] = now + timedelta(seconds=self.block_duration)
            return False
        
        return True
    
    def get_client_quota(self, client_ip: str) -> Dict:
        """Pobranie kwoty klienta"""
        now = datetime.now()
        requests = self.client_requests[client_ip]
        one_minute_ago = now - timedelta(minutes=1)
        
        recent_requests = sum(1 for r in requests if r > one_minute_ago)
        remaining = max(0, self.requests_per_minute - recent_requests)
        
        return {
            'client_ip': client_ip,
            'limit_per_minute': self.requests_per_minute,
            'used': recent_requests,
            'remaining': remaining,
            'is_blocked': client_ip in self.blocked_clients
        }


def test_load_balancer():
    """Test Load Balancera"""
    print("\n🔧 Testowanie Load Balancer...")
    
    # Tworzenie LB
    lb = LoadBalancer('dark8-lb', LoadBalancingAlgorithm.LEAST_CONNECTIONS)
    
    # Dodawanie backendu
    for i in range(3):
        backend = Backend(
            id=f'backend-{i}',
            host=f'server-{i}.dark8.local',
            port=8080 + i,
            weight=1.0
        )
        lb.add_backend(backend)
    
    print(f"✅ Backendu dodane: {len(lb.backends)}")
    
    # Symulacja żądań
    for i in range(10):
        client_ip = f"192.168.1.{i % 5}"
        backend = lb.select_backend(client_ip)
        if backend:
            host, port = lb.handle_request(client_ip)
            print(f"✅ Żądanie od {client_ip} -> {host}:{port}")
    
    # Statystyki
    stats = lb.get_stats()
    print(f"✅ Stats: {stats}")
    
    # Health monitoring
    monitor = HealthMonitor(lb)
    health = monitor.check_all_backends()
    print(f"✅ Health checks: {health}")
    
    # Rate limiting
    rate_limiter = RateLimiter(100)
    for i in range(5):
        allowed = rate_limiter.is_allowed("192.168.1.1")
        print(f"✅ Rate limit check {i}: {allowed}")


if __name__ == '__main__':
    test_load_balancer()
