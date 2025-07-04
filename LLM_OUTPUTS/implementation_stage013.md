# Stage 13: Basic API Tests Setup - Implementation Guide

## Overview
Set up pytest testing framework with test database configuration and basic test structure. This establishes the foundation for comprehensive API testing and ensures code quality through automated testing.

## Prerequisites Completed
- ✅ Stage 12: Database Session Dependencies with enhanced async support
- ✅ All API endpoints functional with proper error handling
- ✅ Database session management with async/sync dual support
- ✅ Health endpoints with database connectivity monitoring

## Objectives
1. Configure pytest with test database support
2. Set up test fixtures for database and API client
3. Create basic health check tests
4. Establish testing patterns for future test development
5. Configure test environment isolation
6. Add test data factories for consistent test data

## Current State Analysis
The current implementation has:
- ✅ Functional API endpoints with proper error handling
- ✅ Async database session management working correctly
- ✅ SQLite database with proper migrations
- ✅ Health check endpoints providing database status
- ❓ No automated testing framework configured
- ❓ Need test database isolation
- ❓ Require test fixtures and utilities

## Implementation Steps

### Step 1: Install Testing Dependencies

Update `pixi.toml` to include testing dependencies:

```toml
[dependencies]
# ... existing dependencies
pytest = ">=7.0.0"
pytest-asyncio = ">=0.21.0"
httpx = ">=0.24.0"  # For async API testing
```

### Step 2: Configure Test Environment

Create `backend/tests/__init__.py`:

```python
"""Tests package for The Sauce Bottle API."""
```

Create `backend/tests/conftest.py` - Main test configuration:

```python
"""Test configuration and fixtures."""
import os
import tempfile
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from backend.main import app
from backend.app.database import Base, get_db
from backend.app.database_async import get_async_db
from backend.app.core.config import settings


# Test database setup
@pytest.fixture(scope="session")
def test_db_url():
    """Create a temporary SQLite database for testing."""
    # Create temporary file for test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    
    # Return SQLite URL for test database
    test_url = f"sqlite:///{db_path}"
    yield test_url
    
    # Cleanup: remove test database file
    try:
        os.unlink(db_path)
    except OSError:
        pass


@pytest.fixture(scope="session")
def test_async_db_url(test_db_url):
    """Get async version of test database URL."""
    return test_db_url.replace("sqlite://", "sqlite+aiosqlite://")


@pytest.fixture(scope="session")
def test_engine(test_db_url):
    """Create test database engine."""
    engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        echo=False  # Set to True for SQL debugging
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup
    engine.dispose()


@pytest.fixture(scope="session")
def test_async_engine(test_async_db_url):
    """Create test async database engine."""
    engine = create_async_engine(
        test_async_db_url,
        connect_args={"check_same_thread": False},
        echo=False
    )
    
    yield engine
    
    # Cleanup
    engine.sync_engine.dispose()


@pytest.fixture
def test_session(test_engine):
    """Create test database session."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest_asyncio.fixture
async def test_async_session(test_async_engine):
    """Create test async database session."""
    TestingAsyncSessionLocal = async_sessionmaker(
        bind=test_async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest.fixture
def client(test_session):
    """Create test client with database dependency override."""
    def override_get_db():
        try:
            yield test_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(test_async_session):
    """Create async test client with database dependency override."""
    async def override_get_async_db():
        yield test_async_session
    
    app.dependency_overrides[get_async_db] = override_get_async_db
    
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()


# Test data fixtures
@pytest.fixture
def sample_politician_data():
    """Sample politician data for testing."""
    return {
        "name": "Test Politician",
        "party": "Test Party",
        "chamber": "House of Representatives",
        "electorate": "Test Electorate",
        "state": "NSW"
    }


@pytest.fixture
def sample_statement_data():
    """Sample statement data for testing."""
    return {
        "content": "This is a test statement",
        "source_url": "https://example.com/statement",
        "source_type": "speech"
    }


@pytest.fixture
def created_politician(client, sample_politician_data):
    """Create a test politician in the database."""
    response = client.post("/api/v1/politicians/", json=sample_politician_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def created_politician_async(async_client, sample_politician_data):
    """Create a test politician in the database (async)."""
    response = await async_client.post("/api/v1/politicians/", json=sample_politician_data)
    assert response.status_code == 201
    return response.json()
```

### Step 3: Basic Health Check Tests

Create `backend/tests/test_main.py`:

```python
"""Tests for main application and health endpoints."""
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_basic_health_check(self, client: TestClient):
        """Test basic health endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "The Sauce Bottle API"
        assert "version" in data
        assert "environment" in data
    
    def test_database_health_check(self, client: TestClient):
        """Test database health endpoint."""
        response = client.get("/api/health/db")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert data["type"] == "SQLite"
        assert "version" in data
    
    def test_migration_health_check(self, client: TestClient):
        """Test migration health endpoint."""
        response = client.get("/api/health/db/migrations")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "migrations_table" in data
    
    @pytest.mark.asyncio
    async def test_async_health_checks(self, async_client: AsyncClient):
        """Test health endpoints with async client."""
        # Test basic health
        response = await async_client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
        # Test database health
        response = await async_client.get("/api/health/db")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestApplicationSetup:
    """Test application configuration and setup."""
    
    def test_api_docs_accessible(self, client: TestClient):
        """Test that API documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_api_openapi_schema(self, client: TestClient):
        """Test OpenAPI schema generation."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert schema["info"]["title"] == "The Sauce Bottle"
        assert "paths" in schema
        assert "/api/v1/politicians/" in schema["paths"]
        assert "/api/v1/statements/" in schema["paths"]
    
    def test_cors_headers(self, client: TestClient):
        """Test CORS configuration."""
        response = client.options("/api/health")
        assert response.status_code == 200
```

### Step 4: Database Test Utilities

Create `backend/tests/test_database.py`:

```python
"""Tests for database functionality and session management."""
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.politician import Politician
from backend.app.models.statement import Statement


class TestDatabaseConnection:
    """Test database connection and basic operations."""
    
    def test_database_session_creation(self, test_session: Session):
        """Test that database session is created correctly."""
        assert test_session is not None
        
        # Test basic query
        result = test_session.execute(text("SELECT 1 as test")).fetchone()
        assert result.test == 1
    
    @pytest.mark.asyncio
    async def test_async_database_session_creation(self, test_async_session: AsyncSession):
        """Test that async database session is created correctly."""
        assert test_async_session is not None
        
        # Test basic query
        result = await test_async_session.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        assert row.test == 1
    
    def test_database_tables_exist(self, test_session: Session):
        """Test that required tables exist in test database."""
        # Check politicians table
        result = test_session.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='politicians'"
        )).fetchone()
        assert result is not None
        
        # Check statements table
        result = test_session.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='statements'"
        )).fetchone()
        assert result is not None
    
    def test_politician_model_creation(self, test_session: Session):
        """Test creating a politician model instance."""
        politician = Politician(
            name="Test Politician",
            party="Test Party",
            chamber="House of Representatives"
        )
        
        test_session.add(politician)
        test_session.commit()
        test_session.refresh(politician)
        
        assert politician.id is not None
        assert politician.name == "Test Politician"
        assert politician.created_at is not None
    
    @pytest.mark.asyncio
    async def test_async_politician_model_creation(self, test_async_session: AsyncSession):
        """Test creating a politician model instance with async session."""
        politician = Politician(
            name="Async Test Politician",
            party="Async Test Party",
            chamber="Senate"
        )
        
        test_async_session.add(politician)
        await test_async_session.commit()
        await test_async_session.refresh(politician)
        
        assert politician.id is not None
        assert politician.name == "Async Test Politician"
        assert politician.created_at is not None


class TestDatabaseRelationships:
    """Test database model relationships."""
    
    def test_politician_statement_relationship(self, test_session: Session):
        """Test relationship between politicians and statements."""
        # Create politician
        politician = Politician(
            name="Relationship Test Politician",
            party="Test Party"
        )
        test_session.add(politician)
        test_session.commit()
        test_session.refresh(politician)
        
        # Create statement
        statement = Statement(
            content="Test statement content",
            politician_id=politician.id
        )
        test_session.add(statement)
        test_session.commit()
        test_session.refresh(statement)
        
        # Test relationship
        assert statement.politician_id == politician.id
        assert len(politician.statements) == 1
        assert politician.statements[0].content == "Test statement content"
```

### Step 5: Test Configuration Files

Update `pixi.toml` to include test commands:

```toml
[tasks]
# ... existing tasks

# Testing tasks
test = "pytest backend/tests/ -v"
test-fast = "pytest backend/tests/ -v -x"  # Stop on first failure
test-cov = "pytest backend/tests/ -v --cov=backend --cov-report=html"
test-health = "pytest backend/tests/test_main.py::TestHealthEndpoints -v"
test-db = "pytest backend/tests/test_database.py -v"
```

Create `backend/pytest.ini`:

```ini
[tool:pytest]
asyncio_mode = auto
testpaths = backend/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

Create `backend/.coveragerc` (for test coverage):

```ini
[run]
source = backend/app
omit = 
    backend/tests/*
    backend/app/__init__.py
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

### Step 6: Test Data Factories

Create `backend/tests/factories.py`:

```python
"""Test data factories for creating consistent test data."""
from datetime import datetime
from typing import Dict, Any

from backend.app.models.politician import Politician
from backend.app.models.statement import Statement


class PoliticianFactory:
    """Factory for creating test politician data."""
    
    @staticmethod
    def build(**kwargs) -> Dict[str, Any]:
        """Build politician data dictionary."""
        defaults = {
            "name": "Test Politician",
            "party": "Test Party",
            "chamber": "House of Representatives",
            "electorate": "Test Electorate",
            "state": "NSW",
            "position_title": None,
            "date_elected": None,
            "sitting_status": "Current",
            "is_cabinet_minister": None,
            "is_shadow_minister": None
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(session, **kwargs) -> Politician:
        """Create politician instance and save to database."""
        data = PoliticianFactory.build(**kwargs)
        politician = Politician(**data)
        session.add(politician)
        session.commit()
        session.refresh(politician)
        return politician


class StatementFactory:
    """Factory for creating test statement data."""
    
    @staticmethod
    def build(politician_id: int = 1, **kwargs) -> Dict[str, Any]:
        """Build statement data dictionary."""
        defaults = {
            "content": "This is a test statement",
            "politician_id": politician_id,
            "source_url": "https://example.com/statement",
            "source_type": "speech",
            "source_name": "Test Source",
            "review_status": "pending",
            "date_made": None,
            "ai_summary": None,
            "ai_contradiction_analysis": None
        }
        defaults.update(kwargs)
        return defaults
    
    @staticmethod
    def create(session, **kwargs) -> Statement:
        """Create statement instance and save to database."""
        data = StatementFactory.build(**kwargs)
        statement = Statement(**data)
        session.add(statement)
        session.commit()
        session.refresh(statement)
        return statement
```

## Testing the Implementation

### Manual Testing Commands

```bash
# Install test dependencies
pixi install

# Run all tests
pixi run test

# Run specific test files
pixi run test-health
pixi run test-db

# Run tests with coverage
pixi run test-cov

# Run tests and stop on first failure
pixi run test-fast
```

### Test Structure Verification

```bash
# Check test discovery
pixi run python -m pytest --collect-only backend/tests/

# Run specific test class
pixi run pytest backend/tests/test_main.py::TestHealthEndpoints -v

# Run with different verbosity levels
pixi run pytest backend/tests/ -v -s
```

## Success Criteria

- ✅ pytest framework configured and running
- ✅ Test database isolation working correctly
- ✅ Basic health check tests passing
- ✅ Database session fixtures functional for both sync and async
- ✅ Test data factories available for consistent test data
- ✅ API client fixtures working for HTTP testing
- ✅ Test coverage reporting configured
- ✅ Test commands available in pixi tasks

## Benefits of This Implementation

1. **Test Isolation**: Each test runs with a clean test database
2. **Async Support**: Tests can use both sync and async database sessions
3. **Fixtures**: Reusable test components reduce code duplication
4. **Data Factories**: Consistent test data generation
5. **Coverage Reporting**: Track test coverage to identify untested code
6. **Multiple Test Types**: Support for unit, integration, and API tests
7. **Easy Commands**: Simple pixi commands for running different test suites

## Next Steps (Stage 14)

After completing this stage, Stage 14 will focus on:
- Politicians API Tests - comprehensive testing of all politician endpoints
- CRUD operation testing with various scenarios
- Error handling and edge case testing
- Data validation testing with invalid inputs