"""Database configuration and connection setup (sync version for migrations)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Generator

from backend.app.core.config import settings

# Create the SQLAlchemy engine for sync operations (mainly migrations)
engine_kwargs = {"echo": settings.DATABASE_ECHO, "future": True}

# Database-specific configuration
if settings.is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
elif settings.is_postgresql:
    engine_kwargs["pool_pre_ping"] = True  # Verify connections before use

# Use sync URL for migrations
engine = create_engine(settings.sync_database_url, **engine_kwargs)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI endpoints (legacy - use async version for new code)
def get_db() -> Generator:
    """
    Get database session (sync version).
    
    Note: This is maintained for backward compatibility and migrations.
    Use get_async_session from database_async.py for new API endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions for database management
def create_tables():
    """Create all tables from models (useful for development)."""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all tables (useful for testing/reset)."""
    Base.metadata.drop_all(bind=engine)

def test_database_connection() -> bool:
    """Test sync database connection."""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False

def get_database_info() -> dict:
    """Get database information (sync version)."""
    with SessionLocal() as session:
        if settings.is_sqlite:
            result = session.execute("SELECT sqlite_version() as version")
            version = result.scalar()
            db_type = "SQLite"
        else:
            result = session.execute("SELECT version()")
            version = result.scalar()
            db_type = "PostgreSQL"
        
        return {
            "type": db_type,
            "version": version,
            "url": settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "local",
            "environment": settings.ENVIRONMENT
        }