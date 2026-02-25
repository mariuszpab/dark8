# DARK8 OS - Persistence Layer (Database & Storage)
"""
Database models, migrations, and storage abstractions.
"""

from datetime import datetime
from typing import Optional, List, Dict

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from dark8_core.config import config
from dark8_core.logger import logger


# SQLAlchemy setup
Base = declarative_base()


# ============================================================================
# Models
# ============================================================================

class Project(Base):
    """Represents a saved project"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    path = Column(String(1024), nullable=False)
    app_type = Column(String(50))  # django, fastapi, react, etc
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)  # Extra data


class Conversation(Base):
    """Represents a user-AI conversation"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    intent = Column(String(100))
    confidence = Column(Float)
    entities = Column(JSON)
    context = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    """Represents an executed task"""
    __tablename__ = "tasks"

    id = Column(String(100), primary_key=True)
    description = Column(Text)
    intent = Column(String(100))
    status = Column(String(20))  # pending, in_progress, completed, failed
    result = Column(Text)
    parameters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)


class KnowledgeItem(Base):
    """Code snippets, patterns, templates in knowledge base"""
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))  # code_snippet, pattern, template, example
    title = Column(String(255))
    content = Column(Text)
    language = Column(String(50))  # python, javascript, java, etc
    tags = Column(JSON)
    embedding = Column(String(4096))  # Vector representation (serialized)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Audit trail for security and debugging"""
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True)
    action = Column(String(100))  # command_executed, file_written, code_generated, etc
    user_input = Column(Text)
    parameters = Column(JSON)
    result = Column(String(20))  # success, error, warning
    error_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


# ============================================================================
# Database Manager
# ============================================================================

class DatabaseManager:
    """Manage database operations"""

    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._init_database()

    def _init_database(self):
        """Initialize database connection"""
        try:
            logger.info(f"Connecting to database: {config.DATABASE_URL}")

            # Create engine
            self.engine = create_engine(
                config.DATABASE_URL,
                echo=config.DEBUG,
                pool_pre_ping=True,
            )

            # Create session factory
            self.SessionLocal = sessionmaker(bind=self.engine)

            # Create tables
            Base.metadata.create_all(self.engine)

            logger.info("✓ Database connected and initialized")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise

    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()

    def add_project(self, name: str, description: str, path: str, app_type: str, metadata: Dict = None) -> Project:
        """Add project to database"""
        session = self.get_session()
        try:
            project = Project(
                name=name,
                description=description,
                path=path,
                app_type=app_type,
                metadata=metadata or {}
            )
            session.add(project)
            session.commit()
            logger.info(f"✓ Project saved: {name}")
            return project
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving project: {e}")
            raise
        finally:
            session.close()

    def get_project(self, name: str) -> Optional[Project]:
        """Get project by name"""
        session = self.get_session()
        try:
            return session.query(Project).filter_by(name=name).first()
        finally:
            session.close()

    def get_all_projects(self) -> List[Project]:
        """Get all projects"""
        session = self.get_session()
        try:
            return session.query(Project).all()
        finally:
            session.close()

    def add_conversation(self, user_input: str, ai_response: str, intent: str, confidence: float, entities: Dict = None, context: Dict = None) -> Conversation:
        """Save conversation"""
        session = self.get_session()
        try:
            conversation = Conversation(
                user_input=user_input,
                ai_response=ai_response,
                intent=intent,
                confidence=confidence,
                entities=entities or {},
                context=context or {}
            )
            session.add(conversation)
            session.commit()
            logger.debug(f"Conversation saved: {intent}")
            return conversation
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving conversation: {e}")
            raise
        finally:
            session.close()

    def get_conversations(self, limit: int = 50) -> List[Conversation]:
        """Get recent conversations"""
        session = self.get_session()
        try:
            return session.query(Conversation).order_by(Conversation.timestamp.desc()).limit(limit).all()
        finally:
            session.close()

    def add_audit_log(self, action: str, user_input: str, parameters: Dict = None, result: str = "success", error_message: str = None) -> AuditLog:
        """Log audit event"""
        session = self.get_session()
        try:
            log = AuditLog(
                action=action,
                user_input=user_input,
                parameters=parameters or {},
                result=result,
                error_message=error_message
            )
            session.add(log)
            session.commit()
            return log
        except Exception as e:
            session.rollback()
            logger.error(f"Error logging audit: {e}")
        finally:
            session.close()


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_database() -> DatabaseManager:
    """Get or create database manager singleton"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


__all__ = [
    "Base",
    "Project",
    "Conversation",
    "Task",
    "KnowledgeItem",
    "AuditLog",
    "DatabaseManager",
    "get_database",
]
