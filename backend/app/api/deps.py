"""Database and API dependencies."""
from typing import AsyncGenerator, Generator
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from backend.app.database import SessionLocal
from backend.app.database_async import get_async_session_local
from backend.app.core.exceptions import DatabaseConnectionError


def get_db() -> Generator[Session, None, None]:
    """
    Get a database session (sync version).
    
    This is maintained for backward compatibility.
    Consider using get_async_db for new endpoints.
    
    Yields:
        Session: SQLAlchemy database session
        
    Raises:
        DatabaseConnectionError: If database connection fails
    """
    db: Session = SessionLocal()
    try:
        # Test the connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseConnectionError() from e
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.
    
    Recommended for new endpoints for better performance.
    
    Yields:
        AsyncSession: Async SQLAlchemy database session
        
    Raises:
        DatabaseConnectionError: If database connection fails
    """
    async with get_async_session_local()() as session:
        try:
            # Test the connection
            from sqlalchemy import text
            await session.execute(text("SELECT 1"))
            yield session
            # Note: AsyncSessionLocal() handles commit/rollback automatically
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseConnectionError() from e
        except Exception as e:
            await session.rollback()
            raise


async def get_async_db_transaction() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session with automatic transaction management.
    
    The transaction will be committed if no exceptions occur,
    otherwise it will be rolled back.
    
    Yields:
        AsyncSession: Async SQLAlchemy database session with transaction
        
    Raises:
        DatabaseConnectionError: If database connection fails
    """
    async with get_async_session_local()() as session:
        try:
            await session.begin()
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise DatabaseConnectionError() from e
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()