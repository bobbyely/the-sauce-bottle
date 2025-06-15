from typing import List, Optional

from sqlalchemy.orm import Session

from backend.app.models.politician import Politician
from backend.app.schemas.politician import PoliticianCreate, PoliticianUpdate


def get(db: Session, politician_id: int) -> Optional[Politician]:
    """Get a politician by ID."""
    return db.query(Politician).filter(Politician.id == politician_id).first()

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Politician]:
    """Get multiple politicians with pagination."""
    return db.query(Politician).offset(skip).limit(limit).all()

def create(db: Session, politician: PoliticianCreate) -> Politician:
    """Create a new politician."""
    db_obj = Politician(**politician.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Politician, obj_in: PoliticianUpdate) -> Politician:
    """Update an existing politician."""
    obj_data = obj_in.model_dump(exclude_unset=True)
    for field, value in obj_data.items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, politician_id: int) -> Optional[Politician]:
    """Remove a politician by ID."""
    db_obj = db.get(Politician, politician_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
