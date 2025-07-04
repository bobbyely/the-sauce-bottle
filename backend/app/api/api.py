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
