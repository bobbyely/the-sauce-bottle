# The Sauce Bottle

The Sauce Bottle is an open-source platform for tracking, analyzing, and exposing statements made by Australian politicians. It combines a FastAPI backend (Python, SQLAlchemy, PostgreSQL) and a Vue.js frontend to collect, organize, and present political statements. The system leverages AI/LLM services to summarize, detect contradictions, and flag misinformation or hypocrisy in statements. The project is designed for transparency, accountability, and public engagement, with a modular architecture supporting robust CRUD operations, authentication, and future AI-powered features. Ideal for researchers, journalists, and civic tech enthusiasts seeking to monitor political discourse in Australia.

## Status and Disclaimer

- This project is a **work in progress**. 
- This project is intended for **educational purposes**. 
- Any analysis carried out by LLMs should be checked for accuracy.

> Fair shake of the sauce bottle! Keep the bastards honest.

# Setup Instructions

- Make sure you have installed `pixi`

## Backend

### Run the backend
From the parent directory:

`pixi run backend-dev`

### Database Setup

**Development Database (SQLite):**
The project now uses SQLite for development - no Docker required!

**Migration Commands:**
```bash
# Apply all pending migrations
pixi run migrate

# Check migration status  
pixi run migrate-status

# Rollback last migration
pixi run migrate-rollback

# Reset database completely
pixi run reset-db
```

### Database Configuration

The project supports both **SQLite** (development) and **PostgreSQL** (production):

**SQLite (Default):**
- Zero setup required - just run the app!
- Perfect for development and testing
- Database file: `saucebottle.db`

**PostgreSQL with Neon (Recommended for production testing):**
1. Sign up for a free Neon account at https://neon.tech
2. Create a new project and get your connection string
3. Add to your `.env` file:
   ```
   POSTGRES_DATABASE_URL=postgresql+asyncpg://username:password@host/database?sslmode=require
   ```
4. Switch between databases easily:
   ```bash
   # Test current database connection
   pixi run db-test
   
   # Show database configuration
   pixi run db-info
   
   # Switch to PostgreSQL
   pixi run db-postgres
   
   # Switch back to SQLite
   pixi run db-sqlite
   ```

**Optional: PostgreSQL with Docker (if you prefer local PostgreSQL):**
```bash
# start it up
docker-compose up -d

# test it
pixi run test-db

# stop it
docker-compose down
```

### Health endpoints
Health endpoints are available under `/api/`:
- [API Health](http://localhost:8000/api/health) - Basic health check
- [Database Health](http://localhost:8000/api/health/db) - Database connectivity
- [Detailed DB Health](http://localhost:8000/api/health/db/detailed) - Table info and statistics
- [Migration Status](http://localhost:8000/api/health/db/migrations) - Check migration status

### API Endpoints
All API endpoints are now organized under `/api/v1/`:
- [Politicians API](http://localhost:8000/api/v1/politicians/)
- [Statements API](http://localhost:8000/api/v1/statements/)
- [API Documentation](http://localhost:8000/api/docs)

### Creating New Migrations

The project uses **Yoyo migrations** for reliable database schema management.

**To create a new migration:**
1. Create a new file in `backend/migrations/` with format: `XXX_description.py`
2. Write the migration using Yoyo's step format:

```python
# backend/migrations/003_add_new_column.py
from yoyo import step

steps = [
    step(
        "ALTER TABLE politicians ADD COLUMN email VARCHAR",  # Forward
        "ALTER TABLE politicians DROP COLUMN email"          # Rollback
    )
]
```

3. Apply the migration: `pixi run migrate`

**Benefits over Alembic:**
- Simple SQL-based approach
- No autogenerate failures  
- Easy to review and understand
- Reliable rollbacks

## Frontend
Coming soon...

# Tests
Run all tests with the following:

```bash
pixi run test

# specifically for backend
pixi run test-backend
```

# API Docs
FastAPI provides automatic interactive API docs.
Once app is running visit /docs and /redocs
e.g. [/docs](http://locahost:8000/docs)

# Contribution Guidelines
This is really a solo project for my own educational purposes. However, I am always
open to learning and suggestion. Please feel free to contact me if you have
an exciting way to point out my naivety. Feel even freer if you are going to suggest
a remedy. Open an Issue to get started.

# Known Issues and TODOs

See the `./LLM_OUTPUTS/development_plan.md` for a thorough list of pending work

There are currently no known issues