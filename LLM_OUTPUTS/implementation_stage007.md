# Implementation Plan: Stage 7 – Politicians API Endpoints

## Objective
Create REST API endpoints for Politicians, enabling CRUD operations via HTTP requests using FastAPI.

## Prerequisites
- Stage 6 completed: Politician CRUD functions implemented and tested.
- Politician Pydantic schemas exist.
- FastAPI app and routing structure in place.

## Deliverables
- `backend/app/api/endpoints/politicians.py`: API routes for Politician
- `backend/app/api/endpoints/__init__.py`: Endpoints package (import Politicians API)
- Integration with main FastAPI app (e.g., include router in `main.py` or central API router)

## Success Criteria
- Can perform CRUD operations on Politicians via HTTP (GET, POST, PUT/PATCH, DELETE)
- Endpoints return correct status codes and use Pydantic schemas for validation/serialization

## Key Code Components
- FastAPI APIRouter for Politician endpoints
- Dependency injection for DB session
- Use of Politician CRUD functions and schemas

---

## Step-by-Step Guide

### 1. Create Endpoints Directory and Files
- Ensure `backend/app/api/endpoints/` exists.
- Create `politicians.py` and (if not present) `__init__.py` in this directory.

### 2. Define APIRouter and Endpoints in `politicians.py`
- Import FastAPI's `APIRouter`, `Depends`, and `HTTPException`.
- Import DB session dependency, Politician CRUD functions, and schemas.
- Create an `APIRouter` instance (e.g., `router = APIRouter(prefix="/politicians", tags=["politicians"])`).
- Implement endpoints:
  - `GET /politicians/` – List all politicians (with pagination)
  - `GET /politicians/{id}` – Get a single politician by ID
  - `POST /politicians/` – Create a new politician
  - `PUT /politicians/{id}` or `PATCH /politicians/{id}` – Update a politician
  - `DELETE /politicians/{id}` – Delete a politician
- Use appropriate response models and status codes.

### 3. Register the Router
- In `backend/app/api/endpoints/__init__.py`, import the router.
- In your main API router or `main.py`, include the politicians router (e.g., `app.include_router(politicians.router)`).

### 4. Test the Endpoints
- Optionally, write or update tests to verify API endpoints work as expected (manual or automated).
- Use FastAPI's interactive docs (`/docs`) to test endpoints.

---

## Example Endpoint Skeleton (Python)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.schemas.politician import Politician, PoliticianCreate, PoliticianUpdate
from backend.app.crud import politician
from backend.app.api.deps import get_db
from typing import List

router = APIRouter(prefix="/politicians", tags=["politicians"])

@router.get("/", response_model=List[Politician])
def read_politicians(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return politician.get_multi(db, skip=skip, limit=limit)

@router.get("/{politician_id}", response_model=Politician)
def read_politician(politician_id: int, db: Session = Depends(get_db)):
    db_pol = politician.get(db, politician_id)
    if not db_pol:
        raise HTTPException(status_code=404, detail="Politician not found")
    return db_pol

@router.post("/", response_model=Politician, status_code=status.HTTP_201_CREATED)
def create_politician(pol_in: PoliticianCreate, db: Session = Depends(get_db)):
    return politician.create(db, pol_in)

@router.put("/{politician_id}", response_model=Politician)
def update_politician(politician_id: int, pol_in: PoliticianUpdate, db: Session = Depends(get_db)):
    db_pol = politician.get(db, politician_id)
    if not db_pol:
        raise HTTPException(status_code=404, detail="Politician not found")
    return politician.update(db, db_pol, pol_in)

@router.delete("/{politician_id}", response_model=Politician)
def delete_politician(politician_id: int, db: Session = Depends(get_db)):
    db_pol = politician.remove(db, politician_id)
    if not db_pol:
        raise HTTPException(status_code=404, detail="Politician not found")
    return db_pol
```

---

## Checklist
- [ ] `api/endpoints/politicians.py` created with all endpoints
- [ ] Router registered in main app
- [ ] Endpoints tested (manual or automated)

---

## Notes
- Use type hints and follow PEP 8 style.
- Document each endpoint with a short docstring.
- Commit changes with a descriptive message (e.g., "Add Politicians API endpoints").
- These endpoints will be used by the frontend and for further API development.
