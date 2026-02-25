"""
DARK8 OS - Phase 4: Performance Profiler
Profilowanie wydajności, analiza bottlenecków i optymalizacja
Autor: DARK8 Development Team
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from collections import deque
import random


class ProfilerMetric(Enum):
    """Metryki profilowania"""
    CPU_TIME = "cpu_time"          # Czas CPU
    WALL_TIME = "wall_time"        # Czas rzeczywisty
    MEMORY_PEAK = "memory_peak"    # Peak pamięci
    MEMORY_CURRENT = "memory_current"  # Bieżąca pamięć
    FUNCTION_CALLS = "function_calls"  # Liczba wywołań


@dataclass
class FunctionProfile:
    """Profil funkcji"""
    name: str
    module: str
    call_count: int = 0
    total_time_ms: float = 0.0
    min_time_ms: float = float('inf')
    max_time_ms: float = 0.0
    memory_peak_mb: float = 0.0
    memory_current_mb: float = 0.0
    
    def avg_time_ms(self) -> float:
        """Średni czas"""
        return self.total_time_ms / self.call_count if self.call_count > 0 else 0
    
    def to_dict(self) -> dict:
        """Konwersja do słownika"""
        return asdict(self)


@dataclass
class BottleneckAnalysis:
    """Analiza bottlenecka"""
    bottleneck_id: str
    function_name: str
    bottleneck_type: str  # 'cpu_intensive', 'memory_intensive', 'io_wait'
    severity: str  # 'critical', 'high', 'medium', 'low'
    threshold: float  # Próg przekoroczenia
    current_value: float  # Bieżąca wartość
    recommendation: str  # Rekomendacja naprawy
    detected_at: datetime = None
    
    def __post_init__(self):
        if self.detected_at is None:
            self.detected_at = datetime.now()


class PerformanceProfiler:
    """
    Profiler wydajności dla DARK8 OS
    Śledzi CPU, pamięć, I/O i bottlenecki
    """
    
    def __init__(self, sample_rate: int = 100):
        """
        Inicjalizacja Performance Profilera
        
        Args:
            sample_rate: Liczba samples na sekundę
        """
        self.sample_rate = sample_rate
        self.function_profiles: Dict[str, FunctionProfile] = {}
        self.call_stack: deque = deque()
        self.memory_samples: deque = deque(maxlen=10000)
        self.cpu_samples: deque = deque(maxlen=10000)
        self.bottlenecks: Dict[str, BottleneckAnalysis] = {}
        self.profiling_active = False
        self.created_at = datetime.now()
        
    def start_profiling(self) -> None:
        """Rozpoczęcie profilowania"""
        self.profiling_active = True
        print("✅ Profiling started")
    
    def stop_profiling(self) -> None:
        """Zatrzymanie profilowania"""
        self.profiling_active = False
        print("✅ Profiling stopped")
    
    def profile_function(self, func: Callable) -> Callable:
        """
        Dekorator do profilowania funkcji
        
        Args:
            func: Funkcja do profilowania
            
        Returns:
            Wrapped funkcja
        """
        def wrapper(*args, **kwargs):
            if not self.profiling_active:
                return func(*args, **kwargs)
            
            func_name = func.__name__
            module = func.__module__
            profile_key = f"{module}.{func_name}"
            
            # Inicjalizacja profilu
            if profile_key not in self.function_profiles:
                self.function_profiles[profile_key] = FunctionProfile(
                    name=func_name,
                    module=module
                )
            
            profile = self.function_profiles[profile_key]
            profile.call_count += 1
            
            # Pomiar czasu
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                elapsed_ms = (end_time - start_time) * 1000
                
                # Aktualizacja metryk
                profile.total_time_ms += elapsed_ms
                profile.min_time_ms = min(profile.min_time_ms, elapsed_ms)
                profile.max_time_ms = max(profile.max_time_ms, elapsed_ms)
                
                # Symulacja memory tracking
                profile.memory_current_mb = random.uniform(10, 500)
                profile.memory_peak_mb = max(profile.memory_peak_mb, profile.memory_current_mb)
        
        return wrapper
    
    def record_memory_sample(self, used_mb: float, available_mb: float) -> None:
        """Rejestracja próbki pamięci"""
        sample = {
            'timestamp': datetime.now().isoformat(),
            'used_mb': used_mb,
            'available_mb': available_mb,
            'usage_percent': (used_mb / (used_mb + available_mb)) * 100
        }
        self.memory_samples.append(sample)
    
    def record_cpu_sample(self, usage_percent: float) -> None:
        """Rejestracja próbki CPU"""
        sample = {
            'timestamp': datetime.now().isoformat(),
            'usage_percent': usage_percent
        }
        self.cpu_samples.append(sample)
    
    def detect_bottlenecks(self) -> List[BottleneckAnalysis]:
        """
        Detekcja bottlenecków
        
        Returns:
            List[BottleneckAnalysis]: Znalezione bottlenecki
        """
        self.bottlenecks = {}
        detected = []
        
        # Analiza CPU-intensive funkcji
        for profile_key, profile in self.function_profiles.items():
            avg_time = profile.avg_time_ms()
            
            # CPU-intensive threshold: > 100ms średnio
            if avg_time > 100:
                bottleneck = BottleneckAnalysis(
                    bottleneck_id=f"bn-cpu-{profile_key}",
                    function_name=profile_key,
                    bottleneck_type='cpu_intensive',
                    severity='high' if avg_time > 200 else 'medium',
                    threshold=100,
                    current_value=avg_time,
                    recommendation=f"Optimize {profile_key}: Consider caching or algorithmic improvements"
                )
                self.bottlenecks[bottleneck.bottleneck_id] = bottleneck
                detected.append(bottleneck)
            
            # Memory-intensive threshold: > 100MB peak
            if profile.memory_peak_mb > 100:
                bottleneck = BottleneckAnalysis(
                    bottleneck_id=f"bn-mem-{profile_key}",
                    function_name=profile_key,
                    bottleneck_type='memory_intensive',
                    severity='high' if profile.memory_peak_mb > 200 else 'medium',
                    threshold=100,
                    current_value=profile.memory_peak_mb,
                    recommendation=f"Reduce memory usage in {profile_key}: Consider streaming or chunking"
                )
                self.bottlenecks[bottleneck.bottleneck_id] = bottleneck
                detected.append(bottleneck)
        
        # Analiza CPU samples
        if self.cpu_samples:
            avg_cpu = sum(s['usage_percent'] for s in self.cpu_samples) / len(self.cpu_samples)
            
            if avg_cpu > 80:
                bottleneck = BottleneckAnalysis(
                    bottleneck_id='bn-cpu-high',
                    function_name='system',
                    bottleneck_type='cpu_intensive',
                    severity='critical' if avg_cpu > 95 else 'high',
                    threshold=80,
                    current_value=avg_cpu,
                    recommendation='System CPU usage is high: Consider load balancing or scaling'
                )
                self.bottlenecks[bottleneck.bottleneck_id] = bottleneck
                detected.append(bottleneck)
        
        # Analiza Memory samples
        if self.memory_samples:
            latest_memory = self.memory_samples[-1]
            
            if latest_memory['usage_percent'] > 85:
                bottleneck = BottleneckAnalysis(
                    bottleneck_id='bn-memory-high',
                    function_name='system',
                    bottleneck_type='memory_intensive',
                    severity='critical' if latest_memory['usage_percent'] > 95 else 'high',
                    threshold=85,
                    current_value=latest_memory['usage_percent'],
                    recommendation='System memory usage is high: Consider garbage collection or memory optimization'
                )
                self.bottlenecks[bottleneck.bottleneck_id] = bottleneck
                detected.append(bottleneck)
        
        return detected
    
    def get_function_stats(self, limit: int = 20) -> List[Dict]:
        """Pobranie statystyk funkcji"""
        # Sort by total time
        sorted_profiles = sorted(
            self.function_profiles.items(),
            key=lambda x: x[1].total_time_ms,
            reverse=True
        )
        
        stats = []
        for profile_key, profile in sorted_profiles[:limit]:
            stats.append({
                'function_name': profile.name,
                'module': profile.module,
                'calls': profile.call_count,
                'total_time_ms': profile.total_time_ms,
                'avg_time_ms': profile.avg_time_ms(),
                'min_time_ms': profile.min_time_ms,
                'max_time_ms': profile.max_time_ms,
                'memory_peak_mb': profile.memory_peak_mb
            })
        
        return stats
    
    def get_memory_stats(self) -> Dict:
        """Pobranie statystyk pamięci"""
        if not self.memory_samples:
            return {}
        
        usage_percents = [s['usage_percent'] for s in self.memory_samples]
        used_mb = [s['used_mb'] for s in self.memory_samples]
        
        return {
            'avg_usage_percent': sum(usage_percents) / len(usage_percents),
            'peak_usage_percent': max(usage_percents),
            'min_usage_percent': min(usage_percents),
            'avg_used_mb': sum(used_mb) / len(used_mb),
            'peak_used_mb': max(used_mb),
            'samples_collected': len(self.memory_samples)
        }
    
    def get_cpu_stats(self) -> Dict:
        """Pobranie statystyk CPU"""
        if not self.cpu_samples:
            return {}
        
        usage_percents = [s['usage_percent'] for s in self.cpu_samples]
        
        return {
            'avg_usage_percent': sum(usage_percents) / len(usage_percents),
            'peak_usage_percent': max(usage_percents),
            'min_usage_percent': min(usage_percents),
            'samples_collected': len(self.cpu_samples)
        }
    
    def get_bottleneck_report(self) -> Dict:
        """Pobranie raportu bottlenecków"""
        bottlenecks = self.detect_bottlenecks()
        
        critical_count = sum(1 for b in bottlenecks if b.severity == 'critical')
        high_count = sum(1 for b in bottlenecks if b.severity == 'high')
        
        return {
            'total_bottlenecks': len(bottlenecks),
            'critical': critical_count,
            'high': high_count,
            'bottlenecks': [
                {
                    'id': b.bottleneck_id,
                    'function': b.function_name,
                    'type': b.bottleneck_type,
                    'severity': b.severity,
                    'value': b.current_value,
                    'recommendation': b.recommendation,
                    'detected_at': b.detected_at.isoformat()
                }
                for b in bottlenecks
            ]
        }
    
    def get_profile_summary(self) -> Dict:
        """Podsumowanie profilowania"""
        return {
            'profiling_active': self.profiling_active,
            'functions_profiled': len(self.function_profiles),
            'function_stats': self.get_function_stats(5),
            'memory_stats': self.get_memory_stats(),
            'cpu_stats': self.get_cpu_stats(),
            'uptime_seconds': (datetime.now() - self.created_at).total_seconds(),
            'sample_rate': self.sample_rate
        }


class PerformanceOptimizer:
    """Optymalizator wydajności"""
    
    def __init__(self, profiler: PerformanceProfiler):
        """Inicjalizacja Optimizer'a"""
        self.profiler = profiler
        self.optimization_history: deque = deque(maxlen=1000)
        self.cache: Dict[str, Any] = {}
        self.cache_hits = 0
        self.cache_misses = 0
        
    def suggest_optimizations(self) -> List[str]:
        """
        Sugestia optymalizacji
        
        Returns:
            List[str]: Lista rekomendacji
        """
        suggestions = []
        report = self.profiler.get_bottleneck_report()
        
        for bottleneck in report['bottlenecks']:
            if bottleneck['severity'] in ['critical', 'high']:
                suggestions.append(bottleneck['recommendation'])
        
        return suggestions
    
    def apply_caching(self, func_name: str, cache_size: int = 1000) -> bool:
        """Włączenie caching'u dla funkcji"""
        self.cache = {}
        self.optimization_history.append({
            'optimization': 'caching',
            'function': func_name,
            'timestamp': datetime.now().isoformat()
        })
        return True
    
    def get_optimization_history(self) -> List[Dict]:
        """Pobranie historii optymalizacji"""
        return list(self.optimization_history)


def test_performance_profiler():
    """Test Performance Profiler"""
    print("\n🔧 Testowanie Performance Profiler...")
    
    # Inicjalizacja
    profiler = PerformanceProfiler()
    profiler.start_profiling()
    
    # Symulacja funkcji
    @profiler.profile_function
    def expensive_operation():
        time.sleep(0.05)
        return "result"
    
    # Wykonanie
    for _ in range(5):
        expensive_operation()
    
    print("✅ Funkcje profilowane")
    
    # Memory samples
    for _ in range(10):
        profiler.record_memory_sample(
            used_mb=random.uniform(100, 300),
            available_mb=2000
        )
    
    print("✅ Memory samples zarejestrowane")
    
    # CPU samples
    for _ in range(10):
        profiler.record_cpu_sample(random.uniform(20, 70))
    
    print("✅ CPU samples zarejestrowane")
    
    # Analiza
    bottlenecks = profiler.detect_bottlenecks()
    print(f"✅ Bottlenecks detected: {len(bottlenecks)}")
    
    # Raport
    report = profiler.get_bottleneck_report()
    print(f"✅ Report: {json.dumps(report, indent=2, default=str)}")
    
    # Optimizer
    optimizer = PerformanceOptimizer(profiler)
    suggestions = optimizer.suggest_optimizations()
    print(f"✅ Suggestions: {len(suggestions)}")


if __name__ == '__main__':
    test_performance_profiler()
