# Implementation Plan: Stage 4 – Statement Model and Table

## Objective
Create the Statement SQLAlchemy model with a relationship to the Politician model, and set up the database migration for the Statement table.

## Prerequisites
- Stage 3 completed: Politician model and table exist in the database.

## Deliverables
- `backend/app/models/statement.py`: SQLAlchemy model for Statement
- Alembic migration for Statement table
- Foreign key relationship to Politician

## Success Criteria
- Statement table is created in the database with a foreign key to the Politician table.

## Key Code Components
- SQLAlchemy model with fields: id, text/content, date, politician_id (foreign key), ai_summary, ai_contradiction_analysis, etc.

---

## Step-by-Step Guide

### 1. Design the Statement Model
- Create `backend/app/models/statement.py`.
- Define a `Statement` class inheriting from `Base` (SQLAlchemy declarative base).
- Fields to include:
  - `id`: Integer, primary key
  - `content` or `text`: String/Text, not null (the statement itself)
  - `date_made`: Date or DateTime, nullable (when the statement was made)
  - `politician_id`: Integer, foreign key to `politicians.id`, not null
  - `ai_summary`: String/Text, nullable (AI-generated summary)
  - `ai_contradiction_analysis`: String/Text, nullable (AI contradiction analysis)
  - `created_at`: DateTime, default to now
  - `updated_at`: DateTime, auto-update on change
- Add `__tablename__ = "statements"`.
- Set up the relationship to the Politician model using SQLAlchemy's `relationship` and `ForeignKey`.

### 2. Update Models Package
- Ensure `backend/app/models/__init__.py` imports the Statement model so Alembic can detect it.

### 3. Create Alembic Migration
- Generate a new migration for the Statement table:
  ```bash
  alembic -c backend/alembic.ini revision --autogenerate -m "create statement table"
  ```
- Review the migration script to ensure:
  - The `statements` table is created with all fields.
  - The `politician_id` column is a foreign key referencing `politicians.id`.
- Apply the migration:
  ```bash
  alembic -c backend/alembic.ini upgrade head
  ```

### 4. Test Table Creation
- Use `psql` or a database tool to verify the `statements` table exists and has the correct columns and foreign key.
- Optionally, add a simple test to create and query a Statement instance linked to a Politician.

---

## Example Statement Model (Python)
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Statement(Base):
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    date_made = Column(Date, nullable=True)
    politician_id = Column(Integer, ForeignKey("politicians.id"), nullable=False)
    ai_summary = Column(Text, nullable=True)
    ai_contradiction_analysis = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    politician = relationship("Politician", back_populates="statements")
```

---

## Checklist
- [ ] `statement.py` model created
- [ ] `__init__.py` updated
- [ ] Alembic migration generated and applied
- [ ] Table creation and relationship verified

---

## Notes
- Use type hints and follow PEP 8 style.
- Document the model class and fields.
- Commit changes with a descriptive message (e.g., "Add Statement model and migration").
- If you add a `statements` relationship to the Politician model, use:
  ```python
  statements = relationship("Statement", back_populates="politician")
  ```
  in the `Politician` class.
