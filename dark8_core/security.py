# DARK8 OS - Security & Input Validation
"""
Security layer with input validation, sanitization, and protection.
"""

from typing import Any, Dict, Optional
import re

from dark8_core.logger import logger


class InputValidator:
    """Validate and sanitize user inputs"""
    
    @staticmethod
    def validate_command(command: str) -> bool:
        """Validate command input"""
        if not command or len(command) == 0:
            return False
        if len(command) > 10000:
            logger.warning("Command too long")
            return False
        return True
    
    @staticmethod
    def validate_filepath(path: str) -> bool:
        """Validate file path for security"""
        # Prevent path traversal
        if ".." in path:
            logger.warning(f"Path traversal attempt: {path}")
            return False
        if path.startswith("/etc") or path.startswith("/sys"):
            logger.warning(f"System path access denied: {path}")
            return False
        return True
    
    @staticmethod
    def validate_code(code: str) -> Dict[str, Any]:
        """Validate code for security issues"""
        issues = []
        
        # Check for dangerous patterns
        dangerous_patterns = [
            r"__import__\(",
            r"eval\(",
            r"exec\(",
            r"os\.system\(",
            r"subprocess\.call\(",
            r"open\(.*'w'",  # File write
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                issues.append(f"⚠️ Dangerous pattern detected: {pattern}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "severity": "high" if issues else "none",
        }


class RateLimiter:
    """Rate limiting for API endpoints"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        import time
        
        now = time.time()
        cutoff = now - self.window_seconds
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > cutoff
        ]
        
        if len(self.requests[client_id]) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for {client_id}")
            return False
        
        self.requests[client_id].append(now)
        return True


class AuditLogger:
    """Log all security-relevant actions"""
    
    def __init__(self, db=None):
        self.db = db
    
    def log_operation(
        self,
        action: str,
        user: str,
        resource: str,
        result: str,
        details: Optional[Dict] = None
    ):
        """Log security-relevant operation"""
        
        log_entry = {
            "action": action,
            "user": user,
            "resource": resource,
            "result": result,
            "details": details or {},
            "timestamp": str(__import__("datetime").datetime.now()),
        }
        
        logger.info(f"🔐 AUDIT: {action} on {resource} - {result}")
        
        if self.db:
            try:
                self.db.add_audit_log(
                    action=action,
                    parameters={"user": user, "resource": resource},
                    result=result,
                    error_message=None
                )
            except Exception as e:
                logger.error(f"Audit logging failed: {e}")


class SecurityContext:
    """Security context for operations"""
    
    def __init__(self, user: str = "system", role: str = "user"):
        self.user = user
        self.role = role
        self.permissions = self._get_permissions(role)
    
    def _get_permissions(self, role: str) -> set:
        """Get permissions for role"""
        permissions_map = {
            "admin": {"read", "write", "delete", "execute", "deploy"},
            "developer": {"read", "write", "execute"},
            "user": {"read", "execute"},
            "guest": {"read"},
        }
        return permissions_map.get(role, {"read"})
    
    def can_execute(self, operation: str) -> bool:
        """Check if operation is allowed"""
        return operation in self.permissions
    
    def require_permission(self, operation: str) -> bool:
        """Require permission or raise error"""
        if not self.can_execute(operation):
            logger.error(f"Permission denied for {self.user}: {operation}")
            return False
        return True


__all__ = [
    "InputValidator",
    "RateLimiter",
    "AuditLogger",
    "SecurityContext",
]
