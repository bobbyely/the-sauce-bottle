# The Sauce Bottle

> Fair shake of the sauce bottle! Keep the bastards honest.

This is a work in progress. 

# Setup

- Make sure you have installed `pixi`


# Run the backend
From the parent directory:

`pixi run backend-dev`

# Start the database

```bash
# start it up
docker-compose up -d

# test it
pixi run test-db

# stop it
docker-compose down
```

# Health endpoints
There are a couple of health endpoints currently setup (API/health)
You can visit, once backend-dev is running, with:
[health](http://localhost:8000/health)
[db-health](http://localhost:8000/db-health)

# DB Migration examples
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

# Tests
Run all tests with the following:

```bash
pixi run test

# specifically for backend
pixi run test-backend
```