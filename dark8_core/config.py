# DARK8 OS - Configuration Module
# Centralized system configuration

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None


# Load environment variables from .env if python-dotenv is available
_env_file = Path(__file__).parent.parent / ".env"
if load_dotenv and _env_file.exists():
    try:
        load_dotenv(_env_file)
    except Exception:
        # Fail silently if dotenv cannot be processed in constrained env
        pass


@dataclass
class SystemConfig:
    """Main system configuration"""

    # Environment
    ENVIRONMENT: str = field(default_factory=lambda: os.getenv("DARK8_ENV", "development"))
    DEBUG: bool = field(default_factory=lambda: os.getenv("DARK8_DEBUG", "true").lower() == "true")
    LOG_LEVEL: str = field(default_factory=lambda: os.getenv("DARK8_LOG_LEVEL", "INFO"))

    # Paths
    PROJECT_ROOT: Path = field(default_factory=lambda: Path(__file__).parent.parent)
    DATA_DIR: Path = field(
        default_factory=lambda: Path(
            os.path.expanduser(os.getenv("DARK8_DATA_DIR", "~/.dark8/data"))
        )
    )
    CACHE_DIR: Path = field(
        default_factory=lambda: Path(
            os.path.expanduser(os.getenv("DARK8_CACHE_DIR", "~/.dark8/cache"))
        )
    )
    LOG_DIR: Path = field(
        default_factory=lambda: Path(
            os.path.expanduser(os.getenv("DARK8_LOG_DIR", "~/.dark8/logs"))
        )
    )

    # Ollama Configuration
    OLLAMA_HOST: str = field(
        default_factory=lambda: os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )
    OLLAMA_MODEL: str = field(default_factory=lambda: os.getenv("OLLAMA_MODEL", "mistral"))
    OLLAMA_TEMPERATURE: float = field(
        default_factory=lambda: float(os.getenv("OLLAMA_TEMPERATURE", "0.3"))
    )
    OLLAMA_CONTEXT_WINDOW: int = field(
        default_factory=lambda: int(os.getenv("OLLAMA_CONTEXT_WINDOW", "8096"))
    )

    # Database
    DATABASE_URL: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./dark8.db")
    )

    # Redis Cache
    REDIS_URL: str = field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )
    REDIS_ENABLED: bool = field(
        default_factory=lambda: os.getenv("REDIS_ENABLED", "false").lower() == "true"
    )

    # Vector Database (Chroma)
    CHROMA_DB_PATH: Path = field(
        default_factory=lambda: Path(
            os.path.expanduser(os.getenv("CHROMA_DB_PATH", "~/.dark8/vector_db"))
        )
    )
    CHROMA_ENABLED: bool = field(
        default_factory=lambda: os.getenv("CHROMA_ENABLED", "true").lower() == "true"
    )

    # Browser
    BROWSER_HEADLESS: bool = field(
        default_factory=lambda: os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
    )
    BROWSER_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("BROWSER_TIMEOUT", "30")))
    DUCKDUCKGO_ENABLED: bool = field(
        default_factory=lambda: os.getenv("DUCKDUCKGO_ENABLED", "true").lower() == "true"
    )

    # API Server
    API_HOST: str = field(default_factory=lambda: os.getenv("API_HOST", "0.0.0.0"))
    API_PORT: int = field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))
    API_RELOAD: bool = field(
        default_factory=lambda: os.getenv("API_RELOAD", "true").lower() == "true"
    )

    # NLP Configuration
    NLP_MODEL_NAME: str = field(
        default_factory=lambda: os.getenv("NLP_MODEL_NAME", "bert-base-multilingual-cased")
    )
    NLP_INTENT_THRESHOLD: float = field(
        default_factory=lambda: float(os.getenv("NLP_INTENT_THRESHOLD", "0.7"))
    )
    NLP_ENTITY_THRESHOLD: float = field(
        default_factory=lambda: float(os.getenv("NLP_ENTITY_THRESHOLD", "0.5"))
    )

    # Security
    SECRET_KEY: str = field(
        default_factory=lambda: os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    )
    JWT_ALGORITHM: str = field(default_factory=lambda: os.getenv("JWT_ALGORITHM", "HS256"))
    JWT_EXPIRATION_HOURS: int = field(
        default_factory=lambda: int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    )

    def __post_init__(self):
        """Create necessary directories"""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

        if self.CHROMA_ENABLED:
            self.CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def get_config() -> SystemConfig:
    """Get singleton config instance"""
    return SystemConfig()


# Convenience access
config = get_config()

__all__ = ["SystemConfig", "get_config", "config"]
