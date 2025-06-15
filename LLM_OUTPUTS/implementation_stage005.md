# Implementation Plan: Stage 5 – Pydantic Schemas

## Objective
Create Pydantic request/response schemas for Politician and Statement API endpoints to ensure data validation and serialization.

## Prerequisites
- Stage 4 completed: Statement model and table exist in the database.
- Politician model and table exist.

## Deliverables
- `backend/app/schemas/politician.py`: Politician schemas
- `backend/app/schemas/statement.py`: Statement schemas
- `backend/app/schemas/__init__.py`: Schemas package

## Success Criteria
- Schemas validate input/output data correctly for both Politician and Statement endpoints.
- All required and optional fields are represented with correct types and validation.

## Key Code Components
- Pydantic BaseModel classes for create, update, and response schemas for both Politician and Statement.

---

## Step-by-Step Guide

### 1. Create Schemas Directory and Files
- Create a new directory: `backend/app/schemas/` (if it does not exist).
- Create `politician.py`, `statement.py`, and `__init__.py` inside this directory.

### 2. Define Politician Schemas
- In `politician.py`, define:
  - `PoliticianBase`: Shared fields (e.g., name, party, position, etc.)
  - `PoliticianCreate`: Inherits from `PoliticianBase`, for creation (may require fields like name, party, etc.)
  - `PoliticianUpdate`: Inherits from `PoliticianBase`, all fields optional for PATCH/PUT
  - `Politician`: Inherits from `PoliticianBase`, adds id and other DB fields, sets `orm_mode = True`

### 3. Define Statement Schemas
- In `statement.py`, define:
  - `StatementBase`: Shared fields (e.g., content, date_made, ai_summary, etc.)
  - `StatementCreate`: Inherits from `StatementBase`, for creation (requires content, politician_id, etc.)
  - `StatementUpdate`: Inherits from `StatementBase`, all fields optional
  - `Statement`: Inherits from `StatementBase`, adds id, created_at, updated_at, sets `orm_mode = True`

### 4. Update Schemas Package
- In `schemas/__init__.py`, import all relevant schemas for easy access.

### 5. Test Schema Validation
- Optionally, write simple unit tests or use FastAPI's interactive docs to verify schema validation and serialization.

---

## Example Politician Schema (Python)
```python
from pydantic import BaseModel
from typing import Optional

class PoliticianBase(BaseModel):
    name: str
    party: Optional[str] = None
    position: Optional[str] = None
    # ...other fields...

class PoliticianCreate(PoliticianBase):
    name: str

class PoliticianUpdate(PoliticianBase):
    pass  # All fields optional

class Politician(PoliticianBase):
    id: int
    class Config:
        orm_mode = True
```

## Example Statement Schema (Python)
```python
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class StatementBase(BaseModel):
    content: str
    date_made: Optional[date] = None
    ai_summary: Optional[str] = None
    ai_contradiction_analysis: Optional[str] = None
    # ...other fields...

class StatementCreate(StatementBase):
    content: str
    politician_id: int

class StatementUpdate(StatementBase):
    pass  # All fields optional

class Statement(StatementBase):
    id: int
    politician_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True
```

---

## Checklist
- [ ] `schemas/politician.py` created with all required schemas
- [ ] `schemas/statement.py` created with all required schemas
- [ ] `schemas/__init__.py` updated
- [ ] Schemas tested for validation and serialization

---

## Notes
- Use type hints and follow PEP 8 style.
- Document each schema class and field.
- Commit changes with a descriptive message (e.g., "Add Pydantic schemas for Politician and Statement").
- These schemas will be used in API endpoints for request validation and response serialization.
