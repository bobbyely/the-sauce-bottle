# Stage 11: Basic API Error Handling - Implementation Guide

## Overview
Implement consistent error responses and exception handling across all API endpoints to provide a professional, predictable error experience for API consumers.

## Prerequisites Completed
- ✅ Stage 10: API Router Integration with `/api/v1/` structure
- ✅ Yoyo migrations setup and working
- ✅ SQLite development database
- ✅ All CRUD endpoints functional

## Objectives
1. Create custom exception classes for common business logic errors
2. Implement consistent error response schemas
3. Add global exception handlers to the FastAPI app
4. Update existing endpoints to use consistent error handling
5. Add validation error handling for Pydantic models
6. Test error responses across all endpoints

## Current State Analysis
Currently in the API endpoints:
- Basic HTTPException usage in some endpoints
- Inconsistent error message formats
- No standardized error response schema
- Missing error handling for edge cases
- No custom exception classes for business logic

## Implementation Steps

### Step 1: Create Error Response Schemas

Create `backend/app/schemas/error.py`:

```python
"""Error response schemas for consistent API error handling."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Individual error detail."""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    status_code: int


class ValidationErrorResponse(BaseModel):
    """Validation error response format."""
    error: str = "Validation Error"
    message: str = "The request contains invalid data"
    details: List[ErrorDetail]
    status_code: int = 422
```

### Step 2: Create Custom Exception Classes

Create `backend/app/core/exceptions.py`:

```python
"""Custom exceptions for business logic errors."""
from typing import Optional


class SauceBottleException(Exception):
    """Base exception for The Sauce Bottle application."""
    
    def __init__(self, message: str, status_code: int = 500, details: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class PoliticianNotFoundError(SauceBottleException):
    """Raised when a politician is not found."""
    
    def __init__(self, politician_id: int):
        super().__init__(
            message=f"Politician with id {politician_id} not found",
            status_code=404,
            details={"politician_id": politician_id}
        )


class StatementNotFoundError(SauceBottleException):
    """Raised when a statement is not found."""
    
    def __init__(self, statement_id: int):
        super().__init__(
            message=f"Statement with id {statement_id} not found",
            status_code=404,
            details={"statement_id": statement_id}
        )


class DuplicatePoliticianError(SauceBottleException):
    """Raised when attempting to create a politician that already exists."""
    
    def __init__(self, name: str):
        super().__init__(
            message=f"Politician with name '{name}' already exists",
            status_code=409,
            details={"politician_name": name}
        )


class DatabaseConnectionError(SauceBottleException):
    """Raised when database connection fails."""
    
    def __init__(self):
        super().__init__(
            message="Unable to connect to database",
            status_code=503,
            details={"service": "database"}
        )


class InvalidDateRangeError(SauceBottleException):
    """Raised when date range parameters are invalid."""
    
    def __init__(self, date_from: str, date_to: str):
        super().__init__(
            message=f"Invalid date range: {date_from} to {date_to}",
            status_code=400,
            details={"date_from": date_from, "date_to": date_to}
        )
```

### Step 3: Create Global Exception Handlers

Update `backend/main.py` to include exception handlers:

```python
# Add these imports
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from backend.app.core.exceptions import SauceBottleException
from backend.app.schemas.error import ErrorResponse, ValidationErrorResponse, ErrorDetail

# Add these exception handlers after creating the app

@app.exception_handler(SauceBottleException)
async def sauce_bottle_exception_handler(request: Request, exc: SauceBottleException):
    """Handle custom SauceBottle exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.message,
            details=[ErrorDetail(message=str(v), field=k) for k, v in exc.details.items()] if exc.details else None,
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTPException",
            message=str(exc.detail),
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        details.append(ErrorDetail(
            field=field,
            message=error["msg"],
            code=error["type"]
        ))
    
    return JSONResponse(
        status_code=422,
        content=ValidationErrorResponse(
            details=details,
            status_code=422
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred. Please try again later.",
            status_code=500
        ).model_dump()
    )
```

### Step 4: Update Politicians Endpoints

Update `backend/app/api/endpoints/politicians.py`:

```python
# Add import
from backend.app.core.exceptions import PoliticianNotFoundError, DuplicatePoliticianError

# Update functions to use custom exceptions:

@router.get("/{politician_id}", response_model=Politician)
def read_politician(
    politician_id: int,
    db: Session = Depends(get_db),
) -> Politician:
    """Retrieve a politician by ID."""
    politician = crud_politician.get(db, politician_id)
    if not politician:
        raise PoliticianNotFoundError(politician_id)
    return politician


@router.put("/{politician_id}", response_model=Politician)
def update_politician(
    politician_id: int,
    politician_in: PoliticianUpdate,
    db: Session = Depends(get_db),
) -> Politician:
    """Update an existing politician."""
    db_politician = crud_politician.get(db, politician_id)
    if not db_politician:
        raise PoliticianNotFoundError(politician_id)
    return crud_politician.update(db, db_obj=db_politician, obj_in=politician_in)


@router.delete("/{politician_id}", response_model=Politician)
def delete_politician(
    politician_id: int,
    db: Session = Depends(get_db),
) -> Politician:
    """Delete a politician by ID."""
    db_politician = crud_politician.remove(db, politician_id)
    if not db_politician:
        raise PoliticianNotFoundError(politician_id)
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
        raise PoliticianNotFoundError(politician_id)
    
    # Validate date range if provided
    if date_from and date_to and date_from > date_to:
        raise InvalidDateRangeError(date_from, date_to)
    
    statements = crud_statement.get_multi_by_politician(
        db,
        politician_id=politician_id,
        skip=skip,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
    )
    return statements
```

### Step 5: Update Statements Endpoints

Update `backend/app/api/endpoints/statements.py`:

```python
# Add imports
from backend.app.core.exceptions import StatementNotFoundError, PoliticianNotFoundError

# Update functions:

@router.post("/", response_model=schemas.Statement)
def create_statement(
    *,
    db: Session = Depends(deps.get_db),
    statement_in: schemas.StatementCreate,
) -> schemas.Statement:
    """Create new statement."""
    # Verify politician exists
    politician = crud.politician.get(db, politician_id=statement_in.politician_id)
    if not politician:
        raise PoliticianNotFoundError(statement_in.politician_id)
    
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
        raise StatementNotFoundError(statement_id)
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
        raise StatementNotFoundError(statement_id)
    
    # If updating politician_id, verify new politician exists
    if statement_in.politician_id is not None:
        politician = crud.politician.get(db, politician_id=statement_in.politician_id)
        if not politician:
            raise PoliticianNotFoundError(statement_in.politician_id)
    
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
        raise StatementNotFoundError(statement_id)
    
    statement = crud.statement.remove(db=db, statement_id=statement_id)
    return statement
```

### Step 6: Add Database Error Handling

Update `backend/app/api/endpoints/health.py`:

```python
from backend.app.core.exceptions import DatabaseConnectionError

@router.get("/health/db")
async def database_health():
    """Check database connectivity."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise DatabaseConnectionError()
```

## Testing the Implementation

### Manual Testing Commands

```bash
# Test error responses
curl -X GET http://localhost:8000/api/v1/politicians/999  # Should return 404
curl -X POST http://localhost:8000/api/v1/politicians/ -H "Content-Type: application/json" -d '{}'  # Should return validation error
curl -X POST http://localhost:8000/api/v1/statements/ -H "Content-Type: application/json" -d '{"content":"test","politician_id":999}'  # Should return politician not found

# Test validation errors
curl -X POST http://localhost:8000/api/v1/politicians/ -H "Content-Type: application/json" -d '{"name": ""}'  # Should return validation error
curl -X POST http://localhost:8000/api/v1/statements/ -H "Content-Type: application/json" -d '{"politician_id": "invalid"}'  # Should return validation error
```

### Expected Error Response Format

```json
{
  "error": "PoliticianNotFoundError",
  "message": "Politician with id 999 not found",
  "details": [
    {
      "field": "politician_id",
      "message": "999"
    }
  ],
  "status_code": 404
}
```

## Benefits of This Implementation

1. **Consistent Error Format**: All errors follow the same schema
2. **Meaningful Error Messages**: Clear, actionable error descriptions
3. **Proper HTTP Status Codes**: Correct status codes for different error types
4. **Type Safety**: Pydantic schemas for error responses
5. **Maintainable**: Custom exceptions make code more readable
6. **API Documentation**: FastAPI auto-generates error response docs
7. **Frontend Friendly**: Structured error format easy to handle in UI

## Success Criteria

- ✅ All endpoints return consistent error format
- ✅ Custom exceptions used throughout the application
- ✅ Validation errors properly formatted
- ✅ Database errors handled gracefully
- ✅ HTTP status codes are appropriate
- ✅ Error responses include helpful details
- ✅ API documentation updated with error schemas

## Next Steps (Stage 12)

After completing this stage, Stage 12 will focus on:
- Database Session Dependencies
- Proper session management
- Connection pooling
- Transaction handling