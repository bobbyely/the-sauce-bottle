from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_async_db
from backend.app.crud import politician_async as crud_politician
from backend.app.crud import statement_async as crud_statement
from backend.app.schemas.politician import Politician, PoliticianCreate, PoliticianUpdate
from backend.app.schemas.statement import Statement
from backend.app.core.exceptions import PoliticianNotFoundError

router = APIRouter(tags=["politicians"])

@router.get("/", response_model=List[Politician])
async def read_politicians(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
) -> List[Politician]:
    """Retrieve politicians with pagination."""
    return await crud_politician.get_multi(db, skip=skip, limit=limit)

@router.get("/{politician_id}", response_model=Politician)
async def read_politician(
    politician_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Politician:
    """Retrieve a politician by ID."""
    politician = await crud_politician.get(db, politician_id)
    if not politician:
        raise PoliticianNotFoundError(politician_id)
    return politician

@router.post("/", response_model=Politician, status_code=status.HTTP_201_CREATED)
async def create_politician(
    politician_in: PoliticianCreate,
    db: AsyncSession = Depends(get_async_db),
) -> Politician:
    """Create a new politician."""
    return await crud_politician.create(db, politician=politician_in)

@router.put("/{politician_id}", response_model=Politician)
async def update_politician(
    politician_id: int,
    politician_in: PoliticianUpdate,
    db: AsyncSession = Depends(get_async_db),
) -> Politician:
    """Update an existing politician."""
    db_politician = await crud_politician.get(db, politician_id)
    if not db_politician:
        raise PoliticianNotFoundError(politician_id)
    return await crud_politician.update(db, db_obj=db_politician, obj_in=politician_in)

@router.delete("/{politician_id}", response_model=Politician)
async def delete_politician(
    politician_id: int,
    db: AsyncSession = Depends(get_async_db),
) -> Politician:
    """Delete a politician by ID."""
    db_politician = await crud_politician.remove(db, politician_id)
    if not db_politician:
        raise PoliticianNotFoundError(politician_id)
    return db_politician

@router.get("/{politician_id}/statements", response_model=List[Statement])
async def read_politician_statements(
    politician_id: int,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[str] = Query(None, description="Filter statements from this date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter statements to this date (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_async_db),
) -> List[Statement]:
    """Get all statements for a specific politician with optional date filtering."""
    # Verify politician exists
    politician = await crud_politician.get(db, politician_id=politician_id)
    if not politician:
        raise PoliticianNotFoundError(politician_id)
    
    statements = await crud_statement.get_multi_by_politician(
        db,
        politician_id=politician_id,
        skip=skip,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
    )
    return statements
