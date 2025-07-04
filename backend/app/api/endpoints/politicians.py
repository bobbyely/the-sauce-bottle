from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.crud import politician as crud_politician
from backend.app.crud import statement as crud_statement
from backend.app.schemas.politician import Politician, PoliticianCreate, PoliticianUpdate
from backend.app.schemas.statement import Statement

router = APIRouter(tags=["politicians"])

@router.get("/", response_model=List[Politician])
def read_politicians(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[Politician]:
    """Retrieve politicians with pagination."""
    return crud_politician.get_multi(db, skip=skip, limit=limit)

@router.get("/{politician_id}", response_model=Politician)
def read_politician(
    politician_id: int,
    db: Session = Depends(get_db),
) -> Politician:
    """Retrieve a politician by ID."""
    politician = crud_politician.get(db, politician_id)
    if not politician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Politician not found",
        )
    return politician

@router.post("/", response_model=Politician, status_code=status.HTTP_201_CREATED)
def create_politician(
    politician_in: PoliticianCreate,
    db: Session = Depends(get_db),
) -> Politician:
    """Create a new politician."""
    return crud_politician.create(db, politician=politician_in)

@router.put("/{politician_id}", response_model=Politician)
def update_politician(
    politician_id: int,
    politician_in: PoliticianUpdate,
    db: Session = Depends(get_db),
) -> Politician:
    """Update an existing politician."""
    db_politician = crud_politician.get(db, politician_id)
    if not db_politician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Politician not found",
        )
    return crud_politician.update(db, db_obj=db_politician, obj_in=politician_in)

@router.delete("/{politician_id}", response_model=Politician)
def delete_politician(
    politician_id: int,
    db: Session = Depends(get_db),
) -> Politician:
    """Delete a politician by ID."""
    db_politician = crud_politician.remove(db, politician_id)
    if not db_politician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Politician not found",
        )
    return db_politician

@router.get("/{politician_id}/statements", response_model=List[Statement])
def read_politician_statements(
    politician_id: int,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[str] = Query(None, description="Filter statements from this date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter statements to this date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
) -> List[Statement]:
    """Get all statements for a specific politician with optional date filtering."""
    # Verify politician exists
    politician = crud_politician.get(db, politician_id=politician_id)
    if not politician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Politician with id {politician_id} not found",
        )
    
    statements = crud_statement.get_multi_by_politician(
        db,
        politician_id=politician_id,
        skip=skip,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
    )
    return statements
