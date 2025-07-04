from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import schemas
from backend.app.api.deps import get_async_db
from backend.app.crud import statement_async as crud_statement
from backend.app.crud import politician_async as crud_politician
from backend.app.core.exceptions import StatementNotFoundError, PoliticianNotFoundError

router = APIRouter(tags=["statements"])

@router.get("/", response_model=List[schemas.Statement])
async def read_statements(
    db: AsyncSession = Depends(get_async_db),
    skip: int = 0,
    limit: int = 100,
    politician_id: Optional[int] = Query(None, description="Filter by politician ID"),
) -> List[schemas.Statement]:
    """Retrieve Statements"""
    if politician_id:
        statements = await crud_statement.get_multi_by_politician(
            db, politician_id=politician_id,
            skip=skip, limit=limit,
        )
    else:
        statements = await crud_statement.get_multi(db, skip=skip, limit=limit)
    return statements

@router.post("/", response_model=schemas.Statement)
async def create_statement(
    *,
    db: AsyncSession = Depends(get_async_db),
    statement_in: schemas.StatementCreate,
) -> schemas.Statement:
    """
    Create new statement.
    
    Requires:
    - **content**: The statement text
    - **politician_id**: ID of the politician who made the statement
    - Other optional fields as defined in schema
    """
    # Verify politician exists
    politician = await crud_politician.get(db, politician_id=statement_in.politician_id)
    if not politician:
        raise PoliticianNotFoundError(statement_in.politician_id)
    
    statement = await crud_statement.create(db=db, statement=statement_in)
    return statement


@router.get("/{statement_id}", response_model=schemas.Statement)
async def read_statement(
    *,
    db: AsyncSession = Depends(get_async_db),
    statement_id: int,
) -> schemas.Statement:
    """Get statement by ID."""
    statement = await crud_statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise StatementNotFoundError(statement_id)
    return statement


@router.put("/{statement_id}", response_model=schemas.Statement)
async def update_statement(
    *,
    db: AsyncSession = Depends(get_async_db),
    statement_id: int,
    statement_in: schemas.StatementUpdate,
) -> schemas.Statement:
    """Update a statement."""
    statement = await crud_statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise StatementNotFoundError(statement_id)
    
    # If updating politician_id, verify new politician exists
    if statement_in.politician_id is not None:
        politician = await crud_politician.get(db, politician_id=statement_in.politician_id)
        if not politician:
            raise PoliticianNotFoundError(statement_in.politician_id)
    
    statement = await crud_statement.update(db=db, db_obj=statement, obj_in=statement_in)
    return statement


@router.delete("/{statement_id}", response_model=schemas.Statement)
async def delete_statement(
    *,
    db: AsyncSession = Depends(get_async_db),
    statement_id: int,
) -> schemas.Statement:
    """Delete a statement."""
    statement = await crud_statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise StatementNotFoundError(statement_id)
    
    statement = await crud_statement.remove(db=db, statement_id=statement_id)
    return statement


