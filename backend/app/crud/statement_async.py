"""Async CRUD operations for Statement model."""
from typing import List, Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.statement import Statement
from backend.app.schemas.statement import StatementCreate, StatementUpdate


async def get(db: AsyncSession, statement_id: int) -> Optional[Statement]:
    """Get a statement by ID."""
    result = await db.execute(select(Statement).where(Statement.id == statement_id))
    return result.scalar_one_or_none()


async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Statement]:
    """Get multiple statements with pagination."""
    result = await db.execute(select(Statement).offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_multi_by_politician(
    db: AsyncSession,
    politician_id: int,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> List[Statement]:
    """Get statements by politician with optional date filtering."""
    query = select(Statement).where(Statement.politician_id == politician_id)
    
    if date_from:
        query = query.where(Statement.date_made >= date_from)
    if date_to:
        query = query.where(Statement.date_made <= date_to)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create(db: AsyncSession, statement: StatementCreate) -> Statement:
    """Create a new statement."""
    db_obj = Statement(**statement.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(db: AsyncSession, db_obj: Statement, obj_in: StatementUpdate) -> Statement:
    """Update an existing statement."""
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove(db: AsyncSession, statement_id: int) -> Optional[Statement]:
    """Remove a statement by ID."""
    db_obj = await get(db, statement_id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
    return db_obj