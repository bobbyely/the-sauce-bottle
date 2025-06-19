from typing import List, Optional

from sqlalchemy.orm import Session

from backend.app.models.statement import Statement
from backend.app.schemas.statement import StatementCreate, StatementUpdate


def get(db: Session, statement_id: int) -> Optional[Statement]:
    """Get a statement by ID."""
    return db.query(Statement).filter(Statement.id == statement_id).first()


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Statement]:
    """Get multiple statements with pagination."""
    return db.query(Statement).offset(skip).limit(limit).all()


def get_by_politician(
    db: Session, *, politician_id: int, skip: int = 0, limit: int = 100,
) -> List[Statement]:
    """Get statements by politician ID."""
    return (
        db.query(Statement)
        .filter(Statement.politician_id == politician_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_multi_by_politician(
    db: Session,
    *,
    politician_id: int,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> List[Statement]:
    """Get statements by politician with optional date filtering."""
    query = db.query(Statement).filter(Statement.politician_id == politician_id)
    
    if date_from:
        query = query.filter(Statement.date_made >= date_from)
    if date_to:
        query = query.filter(Statement.date_made <= date_to)
        
    return query.offset(skip).limit(limit).all()


def create(db: Session, statement: StatementCreate) -> Statement:
    """Create a new statement."""
    db_obj = Statement(**statement.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_with_politician(
    db: Session, *, obj_in: StatementCreate, politician_id: int,
) -> Statement:
    """Create statement with explicit politician ID."""
    db_obj = Statement(
        **obj_in.model_dump(),
        politician_id=politician_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Statement, obj_in: StatementUpdate) -> Statement:
    """Update an existing statement."""
    obj_data = obj_in.model_dump(exclude_unset=True)
    for field, value in obj_data.items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def remove(db: Session, statement_id: int) -> Optional[Statement]:
    """Remove a statement by ID."""
    db_obj = db.get(Statement, statement_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
