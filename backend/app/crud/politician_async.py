"""Async CRUD operations for Politician model."""
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.politician import Politician
from backend.app.schemas.politician import PoliticianCreate, PoliticianUpdate


async def get(db: AsyncSession, politician_id: int) -> Optional[Politician]:
    """Get a politician by ID."""
    result = await db.execute(select(Politician).where(Politician.id == politician_id))
    return result.scalar_one_or_none()


async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Politician]:
    """Get multiple politicians with pagination."""
    result = await db.execute(select(Politician).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create(db: AsyncSession, politician: PoliticianCreate) -> Politician:
    """Create a new politician."""
    db_obj = Politician(**politician.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(db: AsyncSession, db_obj: Politician, obj_in: PoliticianUpdate) -> Politician:
    """Update an existing politician."""
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove(db: AsyncSession, politician_id: int) -> Optional[Politician]:
    """Remove a politician by ID."""
    db_obj = await get(db, politician_id)
    if db_obj:
        await db.delete(db_obj)
        await db.commit()
    return db_obj