# Stage 10: API Router Integration - Implementation Guide

## Overview
Organize all API endpoints under a common router with `/api/v1/` prefix to create a properly versioned API structure.

## Prerequisites Completed
- ✅ Stage 9: All API endpoints created (politicians, statements)
- ✅ Health check endpoints exist
- ✅ Main FastAPI app configured in `backend/main.py`
- ✅ Individual routers working with `/api` prefix

## Objectives
1. Create a centralized API router with version prefix
2. Reorganize all endpoints under `/api/v1/` structure
3. Update OpenAPI documentation settings
4. Ensure backward compatibility (optional)
5. Clean up main.py for better organization

## Current State Analysis
Currently in `main.py`:
- Health router included directly
- Politicians router with `/api` prefix
- Statements router with `/api` prefix
- No version management structure

## Implementation Steps

### Step 1: Create Main API Router

Create `backend/app/api/api.py`:

```python
"""Main API router that combines all endpoint routers."""
from fastapi import APIRouter

from backend.app.api.endpoints import politicians, statements

# Create main API router with v1 prefix
api_router = APIRouter(prefix="/api/v1")

# Include all endpoint routers
api_router.include_router(
    politicians.router,
    prefix="/politicians",
    tags=["politicians"],
)

api_router.include_router(
    statements.router,
    prefix="/statements", 
    tags=["statements"],
)
```

### Step 2: Update Individual Router Configurations

Update `backend/app/api/endpoints/politicians.py`:
```python
# Remove prefix from router definition since it will be added by parent
router = APIRouter(tags=["politicians"])
# Instead of: router = APIRouter(prefix="/politicians", tags=["politicians"])
```

Update `backend/app/api/endpoints/statements.py`:
```python
# Remove prefix from router definition
router = APIRouter(tags=["statements"])
# Instead of: router = APIRouter(prefix="/statements", tags=["statements"])
```

### Step 3: Create Health Check Router

Create `backend/app/api/endpoints/health.py` (if not exists):
```python
"""Health check endpoints."""
from fastapi import APIRouter
from sqlalchemy import text

from backend.app.api import deps
from backend.app.database import engine

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "sauce-bottle-api"}


@router.get("/health/db")
async def database_health():
    """Check database connectivity."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
```

### Step 4: Update Main Application

Update `backend/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.api.api import api_router
from backend.app.api.endpoints.health import router as health_router

# Create FastAPI application instance
app = FastAPI(
    title="The Sauce Bottle API",
    description="Australian political statement tracking and analysis.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vue.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Favicon route
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("backend/static/favicon.ico")

# Include health check endpoints (no version prefix)
app.include_router(health_router, prefix="/api")

# Include main API router with all versioned endpoints
app.include_router(api_router)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint returning basic API information."""
    return {
        "message": "Welcome to The Sauce Bottle API",
        "version": "0.1.0",
        "docs": "/api/docs",
        "health": "/api/health",
        "api_v1": "/api/v1",
    }


# Run the application (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
```

### Step 5: Update API Initialization Files

Update `backend/app/api/__init__.py`:
```python
"""API module for The Sauce Bottle application."""
from backend.app.api.api import api_router

__all__ = ["api_router"]
```

### Step 6: Optional - Add API Version Info Endpoint

Add to `backend/app/api/api.py`:
```python
@api_router.get("/", tags=["api-info"])
async def api_info():
    """Get API version information."""
    return {
        "version": "1.0",
        "endpoints": {
            "politicians": "/api/v1/politicians",
            "statements": "/api/v1/statements",
        },
    }
```

## Updated Endpoint Structure

After implementation, the API structure will be:
```
/ - Root endpoint
/api/health - Health check
/api/health/db - Database health check
/api/docs - Swagger UI documentation
/api/redoc - ReDoc documentation
/api/openapi.json - OpenAPI schema
/api/v1/ - API version info
/api/v1/politicians/ - Politicians endpoints
/api/v1/politicians/{id}
/api/v1/politicians/{id}/statements
/api/v1/statements/ - Statements endpoints
/api/v1/statements/{id}
```

## Testing the New Structure

### Manual Testing Commands
```bash
# Test health endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/health/db

# Test API v1 info
curl http://localhost:8000/api/v1/

# Test politicians endpoints
curl http://localhost:8000/api/v1/politicians/
curl -X POST http://localhost:8000/api/v1/politicians/ -H "Content-Type: application/json" -d '{"name":"Test Politician","party":"Test Party"}'

# Test statements endpoints  
curl http://localhost:8000/api/v1/statements/
curl http://localhost:8000/api/v1/statements/?politician_id=1

# Check documentation
open http://localhost:8000/api/docs
```

### Update Tests
If tests exist, update the endpoint URLs:
```python
# Old: response = client.get("/api/politicians/")
# New: response = client.get("/api/v1/politicians/")
```

## Benefits of This Structure

1. **API Versioning**: Easy to add v2 endpoints in the future
2. **Clear Organization**: All API endpoints under `/api/v1/`
3. **Documentation**: Swagger UI at consistent location `/api/docs`
4. **Separation**: Health checks separate from versioned API
5. **Scalability**: Easy to add new routers and endpoints

## Common Issues and Solutions

1. **Import Errors**: Ensure all imports use `backend.app` prefix
2. **Router Prefix Duplication**: Remove prefixes from individual routers
3. **Missing Tags**: Ensure all routers have appropriate tags for documentation
4. **CORS Issues**: Update frontend to use new `/api/v1/` endpoints

## Rollback Plan

If issues arise, the changes can be reverted by:
1. Restoring original `main.py`
2. Re-adding prefixes to individual routers
3. Removing `api.py` file

## Next Steps (Stage 11)
- Implement consistent error handling across all endpoints
- Add custom exception classes
- Create error response schemas