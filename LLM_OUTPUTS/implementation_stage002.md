# Stage 2: Database Connection Setup – Implementation Plan

## Objective
Configure PostgreSQL connection using SQLAlchemy for the FastAPI backend.

## Prerequisites
- Stage 1 completed: FastAPI app structure exists and `/health` endpoint works.

## Deliverables
- `backend/app/database.py`: SQLAlchemy engine, session management.
- `backend/app/config.py`: Environment variable-based configuration (database URL, etc).
- Docker Compose file for PostgreSQL service (if not already present).

## Implementation Steps

1. **Create `backend/app/config.py`**
   - Define a `Settings` class using Pydantic’s `BaseSettings` for environment variables.
   - Include `DATABASE_URL` and other relevant config.
   - Load `.env` file if present.

2. **Create `backend/app/database.py`**
   - Set up SQLAlchemy engine using the database URL from config.
   - Create a session factory (`SessionLocal`).
   - Provide a dependency function for FastAPI endpoints to get a DB session.

3. **Update `.gitignore` (if needed)**
   - Ensure `.env` and any local config files are ignored.

4. **Add Docker Compose file**
   - Define a `docker-compose.yml` at the project root with a PostgreSQL service.
   - Set environment variables for DB user, password, and database.

5. **Testing**
   - Add a script or instructions to test DB connection (e.g., create/drop tables).
   - Optionally, add a `/db-health` endpoint for DB connectivity check.

## Success Criteria
- FastAPI app can connect to PostgreSQL via SQLAlchemy.
- Can create and drop tables using the session.
- Docker Compose starts PostgreSQL and exposes it to the backend.
