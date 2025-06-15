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

### Start the database

```bash
# start it up
docker-compose up -d

# test it
pixi run test-db

# stop it
docker-compose down
```

### Health endpoints
There are a couple of health endpoints currently setup (API/health)
You can visit, once backend-dev is running, with:
[health](http://localhost:8000/health)
[db-health](http://localhost:8000/db-health)

### DB Migration examples
For making changes to database models etc, run a migration

```bash
# must be from project root (make sure docker compose up -d has run)
alembic -c backend/alembic.ini revision --autogenerate -m "create politician table"

# Check the migration in alembic/versions/xxxxxx_create_some_table.py

# run the migration
alembic -c backend/alembic.ini upgrade head

# PSQL db
psql -h localhost -U postgres saucebottle  # add postgress password postgres
(psql) \dt  # view tables, confirm tables exist
```

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