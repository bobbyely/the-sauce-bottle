# Stage 9: Statements API Endpoints - Implementation Guide

## Overview
Create REST API endpoints for Statements with full CRUD functionality and proper politician relationship handling.

## Prerequisites Completed
- ✅ Stage 8: Statement CRUD operations (`backend/app/crud/statement.py`)
- ✅ Statement model with politician relationship
- ✅ Statement Pydantic schemas
- ✅ Database session dependency
- ✅ Politicians API endpoints (for reference pattern)

## Objectives
1. Create statement API endpoints with all CRUD operations
2. Handle politician relationships in endpoints
3. Implement filtering by politician
4. Add proper error handling and validation
5. Integrate with main FastAPI router

## Implementation Steps

### Step 1: Create Statements API Endpoints File

Create `backend/app/api/endpoints/statements.py`:

```python
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.app.api import deps

router = APIRouter()


@router.get("/statements", response_model=List[schemas.StatementResponse])
def read_statements(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    politician_id: Optional[int] = Query(None, description="Filter by politician ID"),
) -> List[schemas.StatementResponse]:
    """
    Retrieve statements.
    
    - **skip**: Number of statements to skip (for pagination)
    - **limit**: Maximum number of statements to return
    - **politician_id**: Optional filter by politician ID
    """
    if politician_id:
        statements = crud.statement.get_by_politician(
            db, politician_id=politician_id, skip=skip, limit=limit
        )
    else:
        statements = crud.statement.get_multi(db, skip=skip, limit=limit)
    return statements


@router.post("/statements", response_model=schemas.StatementResponse)
def create_statement(
    *,
    db: Session = Depends(deps.get_db),
    statement_in: schemas.StatementCreate,
) -> schemas.StatementResponse:
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
            detail=f"Politician with id {statement_in.politician_id} not found"
        )
    
    statement = crud.statement.create(db=db, statement=statement_in)
    return statement


@router.get("/statements/{statement_id}", response_model=schemas.StatementResponse)
def read_statement(
    *,
    db: Session = Depends(deps.get_db),
    statement_id: int,
) -> schemas.StatementResponse:
    """
    Get statement by ID.
    """
    statement = crud.statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    return statement


@router.put("/statements/{statement_id}", response_model=schemas.StatementResponse)
def update_statement(
    *,
    db: Session = Depends(deps.get_db),
    statement_id: int,
    statement_in: schemas.StatementUpdate,
) -> schemas.StatementResponse:
    """
    Update a statement.
    """
    statement = crud.statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    
    # If updating politician_id, verify new politician exists
    if statement_in.politician_id is not None:
        politician = crud.politician.get(db, politician_id=statement_in.politician_id)
        if not politician:
            raise HTTPException(
                status_code=404,
                detail=f"Politician with id {statement_in.politician_id} not found"
            )
    
    statement = crud.statement.update(db=db, db_obj=statement, obj_in=statement_in)
    return statement


@router.delete("/statements/{statement_id}", response_model=schemas.StatementResponse)
def delete_statement(
    *,
    db: Session = Depends(deps.get_db),
    statement_id: int,
) -> schemas.StatementResponse:
    """
    Delete a statement.
    """
    statement = crud.statement.get(db=db, statement_id=statement_id)
    if not statement:
        raise HTTPException(status_code=404, detail="Statement not found")
    
    statement = crud.statement.remove(db=db, statement_id=statement_id)
    return statement


@router.get("/politicians/{politician_id}/statements", response_model=List[schemas.StatementResponse])
def read_politician_statements(
    *,
    db: Session = Depends(deps.get_db),
    politician_id: int,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[str] = Query(None, description="Filter statements from this date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter statements to this date (YYYY-MM-DD)"),
) -> List[schemas.StatementResponse]:
    """
    Get all statements for a specific politician with optional date filtering.
    """
    # Verify politician exists
    politician = crud.politician.get(db, politician_id=politician_id)
    if not politician:
        raise HTTPException(
            status_code=404,
            detail=f"Politician with id {politician_id} not found"
        )
    
    statements = crud.statement.get_multi_by_politician(
        db,
        politician_id=politician_id,
        skip=skip,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
    )
    return statements
```

### Step 2: Update API Dependencies

Ensure `backend/app/api/deps.py` exists with database dependency:

```python
from typing import Generator

from backend.app.database import SessionLocal


def get_db() -> Generator:
    """
    Database dependency to get DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 3: Create/Update API __init__.py

Create/update `backend/app/api/endpoints/__init__.py`:

```python
"""API endpoint modules."""
```

### Step 4: Update Main Router Integration

Update `backend/main.py` to include statements router:

```python
from backend.app.api.endpoints import politicians, statements

# After politicians router inclusion
app.include_router(statements.router, prefix="/api")
```

### Step 5: Test the Endpoints

Create a test script or use curl/httpie to test:

```bash
# Create a statement
curl -X POST "http://localhost:8000/api/statements" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "We will take strong action on climate change",
    "politician_id": 1,
    "date_made": "2024-01-15",
    "source_url": "https://example.com/speech",
    "source_type": "speech",
    "source_name": "Parliament House"
  }'

# Get all statements
curl "http://localhost:8000/api/statements"

# Get statements for a specific politician
curl "http://localhost:8000/api/politicians/1/statements"

# Get statements with date filtering
curl "http://localhost:8000/api/politicians/1/statements?date_from=2024-01-01&date_to=2024-12-31"

# Update a statement
curl -X PUT "http://localhost:8000/api/statements/1" \
  -H "Content-Type: application/json" \
  -d '{"content": "Updated statement content"}'

# Delete a statement
curl -X DELETE "http://localhost:8000/api/statements/1"
```

## Key Implementation Details

### 1. Politician Relationship Validation
- Always verify politician exists before creating/updating statements
- Return 404 with clear message if politician not found

### 2. Filtering Options
- Filter statements by politician_id in main endpoint
- Dedicated endpoint for politician's statements with date filtering
- Pagination support with skip/limit parameters

### 3. Error Handling
- 404 for non-existent resources
- 422 for validation errors (handled by Pydantic)
- Clear error messages for debugging

### 4. API Documentation
- Docstrings for OpenAPI/Swagger documentation
- Query parameter descriptions
- Response model specifications

## Testing Checklist

- [ ] Create statement with valid politician_id
- [ ] Create statement fails with invalid politician_id
- [ ] Read all statements with pagination
- [ ] Read statements filtered by politician_id
- [ ] Read single statement by ID
- [ ] Read statement returns 404 for invalid ID
- [ ] Update statement with partial data
- [ ] Update statement politician_id validates new politician
- [ ] Delete statement successfully
- [ ] Delete returns 404 for invalid ID
- [ ] Get politician's statements with date filtering
- [ ] API documentation displays correctly at /docs

## Common Issues and Solutions

1. **Import Errors**: Ensure all imports use `backend.app` prefix
2. **Database Session**: Always use Depends(deps.get_db) for session management
3. **Relationship Loading**: Statement responses should include politician data
4. **Date Filtering**: Ensure date format validation (YYYY-MM-DD)

## Next Steps (Stage 10)
- Organize all API endpoints under common router with `/api/v1/` prefix
- Create centralized API configuration
- Update OpenAPI documentation settings

## Additional Enhancements (Optional)
1. Add sorting options (by date, politician, etc.)
2. Add text search for statement content
3. Add bulk operations endpoints
4. Add response caching for frequently accessed data
5. Add more detailed filtering options (by source_type, review_status, etc.)