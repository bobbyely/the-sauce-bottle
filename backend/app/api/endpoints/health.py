"""Health check endpoints."""
from fastapi import APIRouter
from sqlalchemy import text

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
        # Return error details for debugging, but still return 200 OK
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "note": "Database is currently unavailable",
        }
