"""Define health endpoints for the app."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.database import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "message": "API is running successfully.",
    }


@router.get("/db-health")
def db_health(db: Session = Depends(get_db)):
    """Check the health of the database."""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "message": "Database connection successful.",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
