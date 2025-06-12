# Stage 1 Implementation Guide
## Basic FastAPI Project Structure

### Overview
**Objective**: Set up minimal FastAPI application with proper project structure  
**Time Estimate**: 1-2 hours  
**Prerequisites**: Phase 0 completed (pixi, Docker, Git setup)

---

## Step-by-Step Implementation

### Step 1: Install FastAPI Dependencies (15 minutes)

First, add FastAPI and related dependencies to your `pixi.toml`:

```bash
cd ~/the-sauce-bottle
pixi add fastapi uvicorn python-multipart
```

**Expected Output**: Dependencies added to `pixi.toml` and installed

### Step 2: Create Backend Project Structure (10 minutes)

Create the following directory structure:

```bash
mkdir -p backend/app/api
touch backend/app/__init__.py
touch backend/app/api/__init__.py
touch backend/main.py
```

**Verify Structure**:
```bash
tree backend/
# Should show:
# backend/
# ├── app/
# │   ├── __init__.py
# │   └── api/
# │       └── __init__.py
# └── main.py
```

### Step 3: Create Basic FastAPI Application (20 minutes)

Create `backend/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application instance
app = FastAPI(
    title="The Sauce Bottle API",
    description="Australian politicians statement tracking and analysis",
    version="0.1.0",
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vue.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning basic API information."""
    return {
        "message": "Welcome to The Sauce Bottle API",
        "version": "0.1.0",
        "status": "running"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "message": "API is running successfully"
    }

# Run the application (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 4: Create App Package Structure (15 minutes)

Create `backend/app/__init__.py`:

```python
"""
The Sauce Bottle API Package

This package contains the core application logic for the political
statement tracking and analysis system.
"""

__version__ = "0.1.0"
```

Create `backend/app/api/__init__.py`:

```python
"""
API Package

Contains all API-related modules including endpoints, dependencies,
and routing configuration.
"""
```

### Step 5: Test the Application (20 minutes)

#### Method 1: Direct Python Execution
```bash
cd backend
pixi run python main.py
```

#### Method 2: Using Uvicorn (Recommended)
```bash
cd backend  
pixi run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 6: Verify Endpoints (10 minutes)

Test your endpoints using curl or a web browser:

```bash
# Test root endpoint
curl http://localhost:8000/

# Test health endpoint  
curl http://localhost:8000/health
```

**Expected Responses**:

Root endpoint (`/`):
```json
{
  "message": "Welcome to The Sauce Bottle API",
  "version": "0.1.0", 
  "status": "running"
}
```

Health endpoint (`/health`):
```json
{
  "status": "healthy",
  "message": "API is running successfully"
}
```

### Step 7: Access Interactive API Documentation (5 minutes)

FastAPI automatically generates interactive API documentation:

1. Open browser to `http://localhost:8000/docs` (Swagger UI)
2. Open browser to `http://localhost:8000/redoc` (ReDoc)

Both should show your API endpoints and allow you to test them interactively.

---

## Success Criteria Checklist

- [ ] FastAPI server starts without errors
- [ ] Root endpoint (`/`) returns correct JSON response
- [ ] Health endpoint (`/health`) returns healthy status
- [ ] Interactive API docs accessible at `/docs` and `/redoc`
- [ ] No import errors or Python exceptions
- [ ] Server responds to HTTP requests on port 8000
- [ ] CORS middleware configured (for future frontend integration)

---
## Files Created

After completing this stage, you should have:

```
backend/
├── app/
│   ├── __init__.py          # App package initialization
│   └── api/
│       └── __init__.py      # API package initialization
└── main.py                  # FastAPI application entry point
```

---

## Common Issues & Solutions

### Issue 1: FastAPI Import Error
**Error**: `ModuleNotFoundError: No module named 'fastapi'`  
**Solution**: Ensure you ran `pixi add fastapi uvicorn` and are using `pixi run`

### Issue 2: Port Already in Use
**Error**: `OSError: [Errno 48] Address already in use`  
**Solution**: 
- Kill existing process: `lsof -ti:8000 | xargs kill -9`
- Or use different port: `--port 8001`

### Issue 3: Permission Denied
**Error**: `Permission denied` when binding to port
**Solution**: Use ports above 1024 or run with appropriate permissions

### Issue 4: CORS Issues (Future)
**Error**: Browser blocks frontend requests
**Solution**: Verify CORSMiddleware configuration includes your frontend URL

---

## Testing Your Implementation

### Manual Testing Checklist
1. [ ] Server starts successfully
2. [ ] `/` endpoint returns welcome message
3. [ ] `/health` endpoint returns healthy status  
4. [ ] API documentation loads at `/docs`
5. [ ] No error messages in console
6. [ ] Can stop server with Ctrl+C

### Automated Testing (Optional for Stage 1)
You can create a simple test to verify your endpoints:

```bash
# Install httpx for testing
pixi add httpx

# Create simple test
cat > test_stage1.py << 'EOF'
import httpx

def test_endpoints():
    with httpx.Client(base_url="http://localhost:8000") as client:
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        
        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_endpoints()
EOF

# Run test (with server running in another terminal)
pixi run python test_stage1.py
```

---

## Git Commit

After successful completion:

```bash
git add .
git commit -m "Stage 1: Basic FastAPI project structure

- Set up FastAPI application with proper project structure
- Added root and health check endpoints
- Configured CORS middleware for frontend integration
- Created app and api packages
- Added interactive API documentation
- Verified server startup and endpoint responses"
```

---

## Next Steps

After completing Stage 1, you're ready for **Stage 2: Database Connection Setup**:

1. Install PostgreSQL dependencies
2. Configure database connection string
3. Set up SQLAlchemy engine and session
4. Create Docker Compose with PostgreSQL
5. Test database connectivity

---

## Key Learnings from Stage 1

- FastAPI project structure and organization
- Basic endpoint creation and routing
- CORS configuration for frontend integration  
- Interactive API documentation generation
- Development server configuration with auto-reload
- Package initialization and imports in Python

---

## Resources Used

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/)

---

## Stage 1 Complete! 🎉

You now have a working FastAPI application foundation. The next stage will add database connectivity and begin building the data layer for your political statement tracking system.