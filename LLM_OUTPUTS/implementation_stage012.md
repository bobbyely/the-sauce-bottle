# Stage 12: Database Session Dependencies - Implementation Guide

## Overview
Improve database session management by implementing proper dependency injection for database sessions across all API endpoints. This ensures sessions are properly created, used, and closed for each request.

## Prerequisites Completed
- ✅ Stage 11: Basic API Error Handling with consistent error responses
- ✅ Custom exception classes and global exception handlers
- ✅ Yoyo migrations and SQLite development setup
- ✅ All CRUD endpoints functional with proper error handling

## Objectives
1. Review and optimize database session dependencies
2. Ensure proper session lifecycle management
3. Add database connection health monitoring
4. Implement session-level error handling
5. Add database transaction support for complex operations
6. Test database session handling under various conditions

## Current State Analysis
The current implementation has:
- ✅ Basic database session dependency in `backend/app/api/deps.py`
- ✅ Sessions being used in API endpoints
- ✅ SQLAlchemy engine configuration for SQLite
- ❓ Need to verify session cleanup and error handling
- ❓ May need connection pooling optimization
- ❓ Should add database health monitoring

## Implementation Steps

### Step 1: Review Current Database Dependencies

Check `backend/app/api/deps.py` for current session implementation:

```python
from typing import Generator
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal

def get_db() -> Generator:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 2: Enhanced Database Dependencies

Update `backend/app/api/deps.py` to include better error handling:

```python
"""Database and API dependencies."""
from typing import Generator
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.app.database import SessionLocal
from backend.app.core.exceptions import DatabaseConnectionError


def get_db() -> Generator[Session, None, None]:
    """
    Get database session with proper error handling.
    
    Yields:
        Session: SQLAlchemy database session
        
    Raises:
        DatabaseConnectionError: If database connection fails
    """
    db = SessionLocal()
    try:
        # Test the connection
        db.execute("SELECT 1")
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseConnectionError() from e
    finally:
        db.close()


def get_db_transaction() -> Generator[Session, None, None]:
    """
    Get database session with transaction support.
    
    Yields:
        Session: SQLAlchemy database session with transaction
        
    Raises:
        DatabaseConnectionError: If database connection fails
    """
    db = SessionLocal()
    try:
        db.begin()
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        if isinstance(e, SQLAlchemyError):
            raise DatabaseConnectionError() from e
        raise
    finally:
        db.close()
```

### Step 3: Enhanced Health Check with Database

Update `backend/app/api/endpoints/health.py`:

```python
"""Health check endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.api.deps import get_db
from backend.app.core.exceptions import DatabaseConnectionError

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "healthy", "service": "The Sauce Bottle API"}


@router.get("/health/db")
async def database_health(db: Session = Depends(get_db)):
    """Check database connectivity and responsiveness."""
    try:
        # Test basic query
        result = db.execute(text("SELECT 1 as test")).fetchone()
        
        # Test table access
        politicians_count = db.execute(text("SELECT COUNT(*) FROM politicians")).scalar()
        statements_count = db.execute(text("SELECT COUNT(*) FROM statements")).scalar()
        
        return {
            "status": "healthy",
            "database": "connected",
            "connection_test": result.test if result else None,
            "tables": {
                "politicians": politicians_count,
                "statements": statements_count
            }
        }
    except Exception as e:
        raise DatabaseConnectionError() from e


@router.get("/health/detailed")
async def detailed_health(db: Session = Depends(get_db)):
    """Detailed health check with database info."""
    try:
        # Get database info
        db_info = db.execute(text("SELECT sqlite_version() as version")).fetchone()
        
        # Get table info
        tables = db.execute(text("""
            SELECT name, sql 
            FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name
        """)).fetchall()
        
        return {
            "status": "healthy",
            "database": {
                "type": "SQLite",
                "version": db_info.version if db_info else "unknown",
                "tables": [{"name": table.name, "sql": table.sql} for table in tables]
            },
            "api": {
                "version": "0.1.0",
                "endpoints": [
                    "/api/v1/politicians",
                    "/api/v1/statements",
                    "/api/health"
                ]
            }
        }
    except Exception as e:
        raise DatabaseConnectionError() from e
```

### Step 4: Database Configuration Enhancement

Update `backend/app/database.py` for better session management:

```python
"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool

from backend.app.core.config import settings

# Database engine configuration
engine_kwargs = {
    "echo": settings.DATABASE_ECHO,
    "future": True,
}

# SQLite specific configuration
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs.update({
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    })

# Create engine
engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # Keep objects usable after commit
)

# Create declarative base
Base = declarative_base()


def get_database_url() -> str:
    """Get the current database URL."""
    return str(engine.url)


def test_database_connection() -> bool:
    """Test database connection."""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception:
        return False
```

### Step 5: Configuration Updates

Update `backend/app/core/config.py` to include database configuration:

```python
"""Application configuration."""
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./saucebottle.db"
    DATABASE_ECHO: bool = False  # Set to True for SQL logging
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "The Sauce Bottle"
    VERSION: str = "0.1.0"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

### Step 6: Add Database Utilities

Create `backend/app/core/database_utils.py`:

```python
"""Database utility functions."""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.app.database import SessionLocal, engine
from backend.app.core.exceptions import DatabaseConnectionError


def create_db_session() -> Session:
    """Create a new database session."""
    return SessionLocal()


def test_db_connection() -> bool:
    """Test database connection."""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except SQLAlchemyError:
        return False


def get_db_stats() -> dict:
    """Get database statistics."""
    try:
        with SessionLocal() as db:
            politicians_count = db.execute("SELECT COUNT(*) FROM politicians").scalar()
            statements_count = db.execute("SELECT COUNT(*) FROM statements").scalar()
            
            return {
                "politicians": politicians_count,
                "statements": statements_count,
                "connection_status": "healthy"
            }
    except SQLAlchemyError as e:
        return {
            "connection_status": "error",
            "error": str(e)
        }


def cleanup_db_sessions():
    """Clean up database sessions - useful for testing."""
    engine.dispose()
```

### Step 7: Testing Database Session Management

Create `backend/tests/test_database_sessions.py`:

```python
"""Tests for database session management."""
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from backend.main import app
from backend.app.api.deps import get_db
from backend.app.database import SessionLocal


class TestDatabaseSessions:
    """Test database session management."""
    
    def test_get_db_dependency(self):
        """Test get_db dependency function."""
        db_gen = get_db()
        db = next(db_gen)
        
        assert isinstance(db, Session)
        assert db is not None
        
        # Clean up
        try:
            next(db_gen)
        except StopIteration:
            pass
    
    def test_database_session_in_endpoint(self):
        """Test database session usage in API endpoint."""
        client = TestClient(app)
        
        response = client.get("/api/v1/politicians/")
        assert response.status_code == 200
        
        response = client.get("/api/health/db")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_database_session_error_handling(self):
        """Test database session error handling."""
        client = TestClient(app)
        
        # Test with invalid politician ID
        response = client.get("/api/v1/politicians/999")
        assert response.status_code == 404
        
        # Should still be able to make other requests
        response = client.get("/api/health")
        assert response.status_code == 200
    
    def test_database_health_check(self):
        """Test database health check endpoints."""
        client = TestClient(app)
        
        response = client.get("/api/health/db")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "tables" in data
        
        response = client.get("/api/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert "api" in data
```

## Testing the Implementation

### Manual Testing Commands

```bash
# Test basic health checks
curl -X GET http://localhost:8000/api/health
curl -X GET http://localhost:8000/api/health/db
curl -X GET http://localhost:8000/api/health/detailed

# Test database session handling with multiple requests
curl -X GET http://localhost:8000/api/v1/politicians/ &
curl -X GET http://localhost:8000/api/v1/statements/ &
curl -X GET http://localhost:8000/api/health/db &
wait

# Test error handling
curl -X GET http://localhost:8000/api/v1/politicians/999  # Should return 404
curl -X GET http://localhost:8000/api/health/db  # Should still work
```

### Automated Testing

```bash
# Run database session tests
pixi run test backend/tests/test_database_sessions.py

# Run all tests to ensure nothing is broken
pixi run test
```

## Success Criteria

- ✅ Database sessions properly created and closed for each request
- ✅ Database connection errors handled gracefully
- ✅ Health check endpoints provide detailed database status
- ✅ Session lifecycle properly managed with transactions
- ✅ Database connection pooling optimized for SQLite
- ✅ All tests pass with proper session management
- ✅ No database connection leaks or hanging sessions

## Benefits of This Implementation

1. **Proper Session Management**: Sessions are created and closed correctly
2. **Error Handling**: Database errors are caught and handled gracefully
3. **Health Monitoring**: Can monitor database health and connectivity
4. **Transaction Support**: Support for complex operations requiring transactions
5. **Performance**: Optimized connection pooling and session management
6. **Reliability**: Robust error handling prevents database connection issues
7. **Testing**: Comprehensive tests ensure session management works correctly

## Next Steps (Stage 13)

After completing this stage, Stage 13 will focus on:
- Basic API Tests Setup
- pytest configuration with test database
- Test fixtures for database and API testing
- Foundation for comprehensive testing suite