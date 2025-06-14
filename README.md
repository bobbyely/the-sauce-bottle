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