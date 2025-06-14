# Implementation Plan: Stage 3 – Politician Model and Table

## Objective
Create the Politician SQLAlchemy model and set up the initial database migration for the Politician table.

## Prerequisites
- Stage 2 completed: Database connection and configuration are set up and working.

## Deliverables
- `backend/app/models/politician.py`: SQLAlchemy model for Politician
- `backend/app/models/__init__.py`: Ensure models package is initialized
- Alembic migration for Politician table

## Success Criteria
- Politician table is created in the database via migration

## Key Code Components
- SQLAlchemy model with fields: `id`, `name`, `party`, `position`, etc.

---

## Step-by-Step Plan

### 1. Create the Politician Model
- Create `backend/app/models/politician.py`.
- Define a `Politician` class inheriting from `Base` (SQLAlchemy declarative base).
- Fields:
  - `id`: Integer, primary key
  - `name`: String, not null
  - `party`: String, nullable
  - `position`: String, nullable
  - (Add any other relevant fields as needed)
- Add `__tablename__ = "politicians"`.

### 2. Update Models Package
- Ensure `backend/app/models/__init__.py` imports the Politician model.

### 3. Create Alembic Migration
- If Alembic is not initialized, initialize it in the backend project.
- Generate a new migration for the Politician table.
- Review and edit the migration script if necessary.
- Apply the migration to create the table in the database.

### 4. Test Table Creation
- Use a database tool or SQLAlchemy session to verify the table exists.
- Optionally, add a simple test to create and query a Politician instance.

---

## Example Politician Model (Python)
```python
from sqlalchemy import Column, Integer, String
from backend.app.database import Base

class Politician(Base):
    __tablename__ = "politicians"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    position = Column(String, nullable=True)
    # Add more fields as needed
```

---

## Checklist
- [ ] `politician.py` model created
- [ ] `__init__.py` updated
- [ ] Alembic migration generated and applied
- [ ] Table creation verified

---

## Notes
- Use type hints and follow PEP 8 style.
- Document the model class and fields.
- Commit changes with a descriptive message (e.g., "Add Politician model and migration").
