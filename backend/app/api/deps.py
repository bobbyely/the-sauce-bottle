"""Database dependency for FastAPI."""
from typing import Generator

from sqlalchemy.orm import Session

from backend.app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Get a database session."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensure the session is closed after use
