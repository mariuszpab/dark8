"""
DARK8 OS - Phase 4: API Gateway
Centralna brama API z routingiem, autentykacją i rate limitingiem
Autor: DARK8 Development Team
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import re


class HTTPMethod(Enum):
    """Metody HTTP"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"


class AuthType(Enum):
    """Typy autentykacji"""
    NONE = "none"
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    OAUTH2 = "oauth2"
    BASIC = "basic"


@dataclass
class APIRoute:
    """Definicja trasy API"""
    path: str
    methods: List[HTTPMethod]
    backend_url: str
    auth_type: AuthType = AuthType.NONE
    rate_limit_requests: int = 1000
    rate_limit_period_seconds: int = 60
    timeout_seconds: int = 30
    cache_enabled: bool = False
    cache_ttl_seconds: int = 300
    middlewares: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class APIRequest:
    """Reprezentacja żądania API"""
    request_id: str
    path: str
    method: HTTPMethod
    headers: Dict[str, str]
    body: Any = None
    query_params: Dict[str, str] = field(default_factory=dict)
    client_ip: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class APIResponse:
    """Reprezentacja odpowiedzi API"""
    request_id: str
    status_code: int
    body: Any = None
    headers: Dict[str, str] = field(default_factory=dict)
    response_time_ms: float = 0.0
    cached: bool = False


class APIGateway:
    """
    Centralna brama API
    Zarządza routingiem, autentykacją, rate limitingiem i cachingiem
    """
    
    def __init__(self, name: str = "dark8-api-gateway"):
        """
        Inicjalizacja API Gateway
        
        Args:
            name: Nazwa gateway'u
        """
        self.name = name
        self.routes: Dict[str, APIRoute] = {}
        self.request_log: deque = deque(maxlen=10000)
        self.api_keys: Dict[str, Dict] = {}  # api_key -> {client_id, active, created_at}
        self.cache: Dict[str, Tuple[Any, datetime]] = {}  # path + method -> (response, expiry)
        self.rate_limiters: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))
        self.authentication_providers: Dict[str, Callable] = {}
        self.request_counter = 0
        self.created_at = datetime.now()
        
    def register_route(self, route: APIRoute) -> bool:
        """
        Rejestracja trasy API
        
        Args:
            route: Trasa do zarejestrowania
            
        Returns:
            bool: Czy trasa została zarejestrowana
        """
        route_key = f"{route.path}"
        self.routes[route_key] = route
        return True
    
    def register_api_key(self,
                        api_key: str,
                        client_id: str,
                        scopes: List[str] = None) -> bool:
        """
        Rejestracja API key
        
        Args:
            api_key: Klucz API
            client_id: ID klienta
            scopes: Zakresy dostępu
            
        Returns:
            bool: Czy klucz został zarejestrowany
        """
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        self.api_keys[key_hash] = {
            'client_id': client_id,
            'active': True,
            'scopes': scopes or [],
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'request_count': 0
        }
        return True
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """
        Walidacja API key
        
        Args:
            api_key: Klucz API do walidacji
            
        Returns:
            Dict: Informacje o kluczu lub None
        """
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        if key_hash in self.api_keys:
            key_info = self.api_keys[key_hash]
            
            if key_info['active']:
                # Aktualizacja last_used
                key_info['last_used'] = datetime.now().isoformat()
                key_info['request_count'] += 1
                return key_info
        
        return None
    
    def check_rate_limit(self, client_id: str, route_path: str) -> bool:
        """
        Sprawdzenie rate limitacji
        
        Args:
            client_id: ID klienta
            route_path: Ścieżka trasy
            
        Returns:
            bool: Czy żądanie jest dozwolone
        """
        if route_path not in self.routes:
            return True
        
        route = self.routes[route_path]
        limiter_key = f"{client_id}:{route_path}"
        rate_limiter_deque = self.rate_limiters[limiter_key]
        
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=route.rate_limit_period_seconds)
        
        # Usuń stare żądania
        while rate_limiter_deque and rate_limiter_deque[0] < cutoff_time:
            rate_limiter_deque.popleft()
        
        # Sprawdź limit
        if len(rate_limiter_deque) >= route.rate_limit_requests:
            return False
        
        # Dodaj nowe żądanie
        rate_limiter_deque.append(now)
        return True
    
    def get_cache_key(self, path: str, method: HTTPMethod, params: Dict = None) -> str:
        """Generowanie klucza cache'u"""
        params_str = json.dumps(params or {}, sort_keys=True)
        key = f"{method.value}:{path}:{params_str}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def get_cached_response(self, cache_key: str) -> Optional[Any]:
        """Pobranie odpowiedzi z cache'u"""
        if cache_key in self.cache:
            response, expiry = self.cache[cache_key]
            if datetime.now() < expiry:
                return response
            else:
                del self.cache[cache_key]
        
        return None
    
    def cache_response(self, cache_key: str, response: Any, ttl_seconds: int) -> None:
        """Zapamiętanie odpowiedzi w cache'u"""
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self.cache[cache_key] = (response, expiry)
    
    def route_request(self, request: APIRequest) -> APIResponse:
        """
        Routing i obsłużenie żądania
        
        Args:
            request: Żądanie API
            
        Returns:
            APIResponse: Odpowiedź
        """
        self.request_counter += 1
        request_id = f"req-{self.request_counter}"
        request.request_id = request_id
        request.timestamp = datetime.now()
        
        start_time = time.time()
        
        # Zapis żądania
        self.request_log.append({
            'request_id': request_id,
            'path': request.path,
            'method': request.method.value,
            'client_ip': request.client_ip,
            'timestamp': request.timestamp.isoformat()
        })
        
        try:
            # Znalezienie route'u
            route = self._match_route(request.path, request.method)
            
            if not route:
                return APIResponse(
                    request_id=request_id,
                    status_code=404,
                    body={'error': 'Route not found'}
                )
            
            # Autentykacja
            if route.auth_type != AuthType.NONE:
                auth_result = self._authenticate_request(request, route.auth_type)
                
                if not auth_result:
                    return APIResponse(
                        request_id=request_id,
                        status_code=401,
                        body={'error': 'Unauthorized'}
                    )
            
            # Rate limiting
            client_id = request.headers.get('X-Client-ID', request.client_ip)
            
            if not self.check_rate_limit(client_id, route.path):
                return APIResponse(
                    request_id=request_id,
                    status_code=429,
                    body={'error': 'Rate limit exceeded'},
                    headers={'X-RateLimit-Remaining': '0'}
                )
            
            # Sprawdzenie cache'u
            if route.cache_enabled and request.method == HTTPMethod.GET:
                cache_key = self.get_cache_key(route.path, request.method, request.query_params)
                cached_response = self.get_cached_response(cache_key)
                
                if cached_response:
                    end_time = time.time()
                    return APIResponse(
                        request_id=request_id,
                        status_code=200,
                        body=cached_response,
                        response_time_ms=(end_time - start_time) * 1000,
                        cached=True
                    )
            
            # Symulacja forward'u do backend'u
            response_body = {
                'message': f'Response from {route.backend_url}',
                'timestamp': datetime.now().isoformat()
            }
            
            # Cachowanie odpowiedzi
            if route.cache_enabled and request.method == HTTPMethod.GET:
                cache_key = self.get_cache_key(route.path, request.method, request.query_params)
                self.cache_response(cache_key, response_body, route.cache_ttl_seconds)
            
            end_time = time.time()
            
            return APIResponse(
                request_id=request_id,
                status_code=200,
                body=response_body,
                response_time_ms=(end_time - start_time) * 1000,
                headers={'X-Forwarded-To': route.backend_url}
            )
        
        except Exception as e:
            end_time = time.time()
            return APIResponse(
                request_id=request_id,
                status_code=500,
                body={'error': f'Internal server error: {str(e)}'},
                response_time_ms=(end_time - start_time) * 1000
            )
    
    def _match_route(self, path: str, method: HTTPMethod) -> Optional[APIRoute]:
        """Znalezienie pasującej trasy"""
        # Exact match
        if path in self.routes:
            route = self.routes[path]
            if method in route.methods:
                return route
        
        # Pattern matching (simple wildcard support)
        for route_path, route in self.routes.items():
            if self._match_path_pattern(route_path, path) and method in route.methods:
                return route
        
        return None
    
    def _match_path_pattern(self, pattern: str, path: str) -> bool:
        """Porównanie ścieżki z patternem"""
        # Prosty wildcard matching
        pattern = pattern.replace('*', '.*')
        return re.match(f"^{pattern}$", path) is not None
    
    def _authenticate_request(self, request: APIRequest, auth_type: AuthType) -> bool:
        """Autentykacja żądania"""
        if auth_type == AuthType.API_KEY:
            api_key = request.headers.get('X-API-Key')
            return api_key is not None and self.validate_api_key(api_key) is not None
        
        elif auth_type == AuthType.BEARER_TOKEN:
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
                return len(token) > 0  # Symplifikacja
        
        elif auth_type == AuthType.OAUTH2:
            # Symplifikacja OAuth2
            return request.headers.get('Authorization') is not None
        
        return True  # Dla NONE i BASIC
    
    def get_gateway_stats(self) -> Dict:
        """Statystyki gateway'u"""
        cache_size = len(self.cache)
        cache_memory_estimate = cache_size * 1024  # ~1KB per cached response
        
        return {
            'name': self.name,
            'uptime_seconds': (datetime.now() - self.created_at).total_seconds(),
            'total_requests': self.request_counter,
            'routes_registered': len(self.routes),
            'api_keys_registered': len(self.api_keys),
            'cached_responses': cache_size,
            'cache_memory_estimate_kb': cache_memory_estimate,
            'request_log_entries': len(self.request_log)
        }
    
    def get_request_history(self, limit: int = 50) -> List[Dict]:
        """Pobranie historii żądań"""
        return list(self.request_log)[-limit:]


class RateLimitPolicy:
    """Polityka rate limitacji"""
    
    def __init__(self):
        """Inicjalizacja polityki"""
        self.policies: Dict[str, Dict] = {}
    
    def add_policy(self,
                  policy_name: str,
                  requests_per_minute: int = 1000,
                  burst_size: int = 100,
                  client_type: str = "standard") -> bool:
        """Dodanie polityki"""
        self.policies[policy_name] = {
            'requests_per_minute': requests_per_minute,
            'burst_size': burst_size,
            'client_type': client_type
        }
        return True
    
    def get_policy(self, policy_name: str) -> Optional[Dict]:
        """Pobranie polityki"""
        return self.policies.get(policy_name)


def test_api_gateway():
    """Test API Gateway"""
    print("\n🔧 Testowanie API Gateway...")
    
    gateway = APIGateway()
    
    # Rejestracja tras
    routes = [
        APIRoute(
            path='/api/users',
            methods=[HTTPMethod.GET, HTTPMethod.POST],
            backend_url='http://users-service:8080',
            auth_type=AuthType.API_KEY,
            cache_enabled=True,
            cache_ttl_seconds=300
        ),
        APIRoute(
            path='/api/data',
            methods=[HTTPMethod.GET],
            backend_url='http://data-service:8080',
            cache_enabled=True
        )
    ]
    
    for route in routes:
        gateway.register_route(route)
    
    print(f"✅ Trasy zarejestrowane: {len(gateway.routes)}")
    
    # Rejestracja API key
    gateway.register_api_key('sk_test_123456789', 'client_123')
    print("✅ API key zarejestrowany")
    
    # Żądania testowe
    request1 = APIRequest(
        request_id="",
        path='/api/users',
        method=HTTPMethod.GET,
        headers={'X-API-Key': 'sk_test_123456789', 'X-Client-ID': 'client_123'},
        client_ip='192.168.1.1'
    )
    
    response1 = gateway.route_request(request1)
    print(f"✅ Request 1: Status {response1.status_code}")
    
    # Testowanie cache'u
    response2 = gateway.route_request(request1)
    print(f"✅ Request 2 (cached): Cached={response2.cached}")
    
    # Statystyki
    stats = gateway.get_gateway_stats()
    print(f"✅ Gateway stats: {json.dumps(stats, indent=2)}")
    
    # Historia
    history = gateway.get_request_history(5)
    print(f"✅ Request history: {len(history)} entries")


if __name__ == '__main__':
    test_api_gateway()
