"""Async database configuration and session management."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.pool import NullPool, StaticPool

from backend.app.core.config import settings

# Import the same Base used by models
from backend.app.database import Base

# Global variables for lazy initialization
_async_engine: AsyncEngine = None
_AsyncSessionLocal: async_sessionmaker = None


def get_async_engine() -> AsyncEngine:
    """Get or create the async engine."""
    global _async_engine
    
    if _async_engine is None:
        # Create async engine with environment-specific configuration
        engine_kwargs = {
            "echo": settings.DATABASE_ECHO,
            "future": True,
        }

        # Database-specific configuration
        if settings.is_sqlite:
            # SQLite specific settings
            engine_kwargs.update({
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,  # Use StaticPool for SQLite
            })
        elif settings.is_postgresql:
            # Use NullPool for serverless PostgreSQL (like Neon)
            if settings.is_development and "neon" in settings.DATABASE_URL:
                engine_kwargs.update({
                    "poolclass": NullPool,
                    "pool_pre_ping": True,  # Verify connections before use
                })
            else:
                # Regular PostgreSQL with connection pooling
                engine_kwargs.update({
                    "pool_size": settings.DATABASE_POOL_SIZE,
                    "max_overflow": settings.DATABASE_MAX_OVERFLOW,
                    "pool_pre_ping": True,  # Verify connections before use
                })

        # Create async engine
        _async_engine = create_async_engine(
            settings.async_database_url,
            **engine_kwargs
        )
    
    return _async_engine


def get_async_session_local() -> async_sessionmaker:
    """Get or create the async session factory."""
    global _AsyncSessionLocal
    
    if _AsyncSessionLocal is None:
        # Create async session factory
        _AsyncSessionLocal = async_sessionmaker(
            bind=get_async_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
    
    return _AsyncSessionLocal


# For backward compatibility, expose as module attributes
async_engine = property(lambda: get_async_engine())
AsyncSessionLocal = get_async_session_local


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async session dependency for FastAPI.
    
    Yields:
        AsyncSession: Async database session
    """
    session_factory = get_async_session_local()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def test_database_connection() -> bool:
    """Test async database connection."""
    try:
        engine = get_async_engine()
        async with engine.connect() as conn:
            from sqlalchemy import text
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        # For debugging - log the error
        print(f"Connection test error: {e}")
        return False


async def get_database_info() -> dict:
    """Get database information."""
    from sqlalchemy import text
    
    session_factory = get_async_session_local()
    async with session_factory() as session:
        if settings.is_sqlite:
            result = await session.execute(text("SELECT sqlite_version() as version"))
            version = result.scalar()
            db_type = "SQLite"
        else:
            result = await session.execute(text("SELECT version()"))
            version = result.scalar()
            db_type = "PostgreSQL"
        
        return {
            "type": db_type,
            "version": version,
            "url": settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else "local",
            "async_driver": "aiosqlite" if settings.is_sqlite else "asyncpg"
        }