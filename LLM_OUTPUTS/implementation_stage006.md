# Implementation Plan: Stage 6 – Politicians CRUD Operations

## Objective
Implement database CRUD (Create, Read, Update, Delete) operations for Politicians using SQLAlchemy ORM.

## Prerequisites
- Stage 5 completed: Pydantic schemas for Politician exist.
- Politician model and table exist in the database.

## Deliverables
- `backend/app/crud/politician.py`: CRUD functions for Politician
- `backend/app/crud/__init__.py`: CRUD package (import Politician CRUD)

## Success Criteria
- Can create, read, update, and delete politicians in the database via Python functions.
- Functions are reusable and ready for API integration.

## Key Code Components
- SQLAlchemy query functions: `get`, `get_multi`, `create`, `update`, `delete` for Politician

---

## Step-by-Step Guide

### 1. Create CRUD Directory and Files
- Ensure `backend/app/crud/` directory exists.
- Create `politician.py` and (if not present) `__init__.py` in this directory.

### 2. Implement CRUD Functions in `politician.py`
- Import necessary modules: SQLAlchemy Session, Politician model, Politician schemas.
- Implement the following functions:
  - `get(db: Session, id: int) -> Optional[Politician]`: Get a single politician by ID.
  - `get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Politician]`: Get multiple politicians (with pagination).
  - `create(db: Session, obj_in: PoliticianCreate) -> Politician`: Create a new politician.
  - `update(db: Session, db_obj: Politician, obj_in: PoliticianUpdate) -> Politician`: Update an existing politician.
  - `remove(db: Session, id: int) -> Politician`: Delete a politician by ID.

### 3. Update CRUD Package
- In `crud/__init__.py`, import the Politician CRUD functions for easy access.

### 4. Test CRUD Operations
- Optionally, write simple unit tests or use an interactive Python shell to verify CRUD logic.

---

## Example CRUD Function Signatures
```python
from sqlalchemy.orm import Session
from backend.app.models.politician import Politician
from backend.app.schemas.politician import PoliticianCreate, PoliticianUpdate
from typing import List, Optional

def get(db: Session, id: int) -> Optional[Politician]:
    ...

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Politician]:
    ...

def create(db: Session, obj_in: PoliticianCreate) -> Politician:
    ...

def update(db: Session, db_obj: Politician, obj_in: PoliticianUpdate) -> Politician:
    ...

def remove(db: Session, id: int) -> Politician:
    ...
```

---

## Checklist
- [ ] `crud/politician.py` created with all CRUD functions
- [ ] `crud/__init__.py` updated
- [ ] CRUD functions tested or verified

---

## Notes
- Use type hints and follow PEP 8 style.
- Document each function with a short docstring.
- Commit changes with a descriptive message (e.g., "Add CRUD operations for Politician model").
- These functions will be used in API endpoints in the next stage.
