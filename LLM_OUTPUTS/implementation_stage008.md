# Stage 8: Statements CRUD Operations - Implementation Guide

## Overview
This guide provides detailed implementation instructions for Stage 8 of The Sauce Bottle project. This stage focuses on implementing database operations (CRUD) for the Statement model, following the established patterns from the Politician implementation.

## Prerequisites
- Stage 7 completed (Politicians API Endpoints working)
- Statement model and schemas already defined
- Database migrations applied
- Understanding of the existing CRUD pattern from politician.py

## Time Estimate
1-2 hours

## Deliverables
1. `backend/app/crud/statement.py` - Statement CRUD functions
2. Updated `backend/app/crud/__init__.py` - Export statement CRUD operations

## Implementation Steps

### Step 1: Create Statement CRUD Module

Create `backend/app/crud/statement.py` with the following structure:

```python
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.statement import Statement
from app.schemas.statement import StatementCreate, StatementUpdate


class CRUDStatement(CRUDBase[Statement, StatementCreate, StatementUpdate]):
    """CRUD operations for Statement model."""
    
    def get_by_politician(
        self, db: Session, *, politician_id: int, skip: int = 0, limit: int = 100
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
        self, 
        db: Session, 
        *, 
        politician_id: int, 
        skip: int = 0, 
        limit: int = 100,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> List[Statement]:
        """Get statements by politician with optional date filtering."""
        query = db.query(Statement).filter(Statement.politician_id == politician_id)
        
        if date_from:
            query = query.filter(Statement.date_made >= date_from)
        if date_to:
            query = query.filter(Statement.date_made <= date_to)
            
        return query.offset(skip).limit(limit).all()
    
    def create_with_politician(
        self, db: Session, *, obj_in: StatementCreate, politician_id: int
    ) -> Statement:
        """Create statement with explicit politician ID."""
        db_obj = Statement(
            **obj_in.model_dump(),
            politician_id=politician_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


statement = CRUDStatement(Statement)
```

### Step 2: Create Base CRUD Class (if not exists)

If `backend/app/crud/base.py` doesn't exist, create it:

```python
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
```

### Step 3: Alternative Implementation (Without Base Class)

If you prefer to follow the exact pattern from politician.py (without base class):

```python
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.statement import Statement
from app.schemas.statement import StatementCreate, StatementUpdate


def get(db: Session, statement_id: int) -> Optional[Statement]:
    """Get a statement by ID."""
    return db.query(Statement).filter(Statement.id == statement_id).first()


def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Statement]:
    """Get multiple statements."""
    return db.query(Statement).offset(skip).limit(limit).all()


def get_by_politician(
    db: Session, *, politician_id: int, skip: int = 0, limit: int = 100
) -> List[Statement]:
    """Get statements by politician ID."""
    return (
        db.query(Statement)
        .filter(Statement.politician_id == politician_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(db: Session, *, statement: StatementCreate) -> Statement:
    """Create a new statement."""
    db_statement = Statement(**statement.model_dump())
    db.add(db_statement)
    db.commit()
    db.refresh(db_statement)
    return db_statement


def update(
    db: Session, *, db_statement: Statement, statement: StatementUpdate
) -> Statement:
    """Update a statement."""
    statement_data = statement.model_dump(exclude_unset=True)
    for field, value in statement_data.items():
        setattr(db_statement, field, value)
    db.add(db_statement)
    db.commit()
    db.refresh(db_statement)
    return db_statement


def remove(db: Session, *, statement_id: int) -> Statement:
    """Delete a statement."""
    statement = db.query(Statement).get(statement_id)
    db.delete(statement)
    db.commit()
    return statement
```

### Step 4: Update CRUD Module Exports

Update `backend/app/crud/__init__.py`:

```python
from .politician import (
    get as get_politician,
    get_multi as get_multi_politicians,
    create as create_politician,
    update as update_politician,
    remove as remove_politician,
)
from .statement import (
    get as get_statement,
    get_multi as get_multi_statements,
    get_by_politician as get_statements_by_politician,
    create as create_statement,
    update as update_statement,
    remove as remove_statement,
)

# Or if using class-based approach:
# from .politician import politician
# from .statement import statement
```

### Step 5: Testing the Implementation

Create a test script or use Python REPL to verify:

```python
# Test in Python REPL
from app.database import SessionLocal
from app.crud import statement as crud_statement
from app.schemas.statement import StatementCreate

# Create a test session
db = SessionLocal()

# Test create
test_statement = StatementCreate(
    content="Test statement content",
    source="Test Source",
    date_made="2024-01-01",
    politician_id=1  # Ensure this politician exists
)

created = crud_statement.create(db=db, obj_in=test_statement)
print(f"Created statement: {created.id}")

# Test get
retrieved = crud_statement.get(db=db, id=created.id)
print(f"Retrieved: {retrieved.content}")

# Test get by politician
politician_statements = crud_statement.get_by_politician(
    db=db, politician_id=1
)
print(f"Found {len(politician_statements)} statements for politician 1")

db.close()
```

## Success Criteria Checklist

- [ ] Statement CRUD module created with all basic operations
- [ ] Can create statements with politician relationship
- [ ] Can retrieve statements by ID
- [ ] Can retrieve multiple statements with pagination
- [ ] Can retrieve statements by politician ID
- [ ] Can update existing statements
- [ ] Can delete statements
- [ ] CRUD functions handle database sessions properly
- [ ] All operations commit changes to database
- [ ] Exports added to crud/__init__.py

## Common Issues and Solutions

### Issue 1: Import Errors
**Problem**: Cannot import Statement model or schemas
**Solution**: Ensure __init__.py files exist in all directories and imports are correct

### Issue 2: Foreign Key Constraint
**Problem**: Creating statement fails due to politician_id constraint
**Solution**: Ensure the politician_id exists in the database before creating statement

### Issue 3: Session Management
**Problem**: Database changes not persisting
**Solution**: Ensure db.commit() is called after add/update operations

## Next Steps

After completing this stage:
1. Run manual tests to verify all CRUD operations work
2. Check that relationships with Politician model work correctly
3. Prepare for Stage 9: Statements API Endpoints

## Code Quality Checklist

- [ ] Type hints used for all function parameters and returns
- [ ] Docstrings added to all functions
- [ ] Code follows existing patterns from politician.py
- [ ] No hardcoded values
- [ ] Proper error handling (will be enhanced in Stage 11)

## Additional Features (Optional)

Consider adding these methods if time permits:
- Search statements by content (using LIKE query)
- Get statements by date range
- Bulk create/update operations
- Soft delete functionality