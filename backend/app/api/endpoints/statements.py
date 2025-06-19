from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.app.api import deps

router = APIRouter(prefix="/statements", tags=["statements"])

@router.get("/", response_model=List[schemas.Statement])
def read_statements(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    politician_id: Optional[int] = Query(None, description="Filter by politician ID"),
) -> List[schemas.Statement]:
    """Retrieve Statements"""
    if politician_id:
        statements = crud.statement.get_by_politician(
            db, politician_id=politician_id,
            skip=skip, limit=limit,
        )
    else:
        statements = crud.statement.get_multi(db, skip=skip, limit=limit)
    return statements

@router.post("/", response_model=schemas.Statement)
def create_statement(
    *,
    db: Session = Depends(deps.get_db),
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
    politician = crud.politician.get(db, politician_id=statement_in.politician_id)
    if not politician:
        raise HTTPException(
            status_code=404,
            detail=f"Politician with id {statement_in.politician_id} not found",
        )
    
    statement = crud.statement.create(db=db, statement=statement_in)
    return statement


@router.get("/{statement_id}", response_model=schemas.Statement)
def read_statement(
    *,
    db: Session = Depends(deps.get_db),
    statement_id: int,
) -> schemas.Statement:
    """Get statement by ID."""
    statement = crud.statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    return statement


@router.put("/{statement_id}", response_model=schemas.Statement)
def update_statement(
    *,
    db: Session = Depends(deps.get_db),
    statement_id: int,
    statement_in: schemas.StatementUpdate,
) -> schemas.Statement:
    """Update a statement."""
    statement = crud.statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    
    # If updating politician_id, verify new politician exists
    if statement_in.politician_id is not None:
        politician = crud.politician.get(db, politician_id=statement_in.politician_id)
        if not politician:
            raise HTTPException(
                status_code=404,
                detail=f"Politician with id {statement_in.politician_id} not found",
            )
    
    statement = crud.statement.update(db=db, db_obj=statement, obj_in=statement_in)
    return statement


@router.delete("/{statement_id}", response_model=schemas.Statement)
def delete_statement(
    *,
    db: Session = Depends(deps.get_db),
    statement_id: int,
) -> schemas.Statement:
    """Delete a statement."""
    statement = crud.statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    
    statement = crud.statement.remove(db=db, statement_id=statement_id)
    return statement


