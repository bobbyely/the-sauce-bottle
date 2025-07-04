from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.app.api.api import api_router
from backend.app.api.endpoints.health import router as health_router

# Create FastAPI application instance
app = FastAPI(
    title="The Sauce Bottle API",
    description="Australian political statement tracking and analysis.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vue.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Favicon route
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("backend/static/favicon.ico")

# Include health check endpoints (no version prefix)
app.include_router(health_router, prefix="/api")

# Include main API router with all versioned endpoints
app.include_router(api_router)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint returning basic API information."""
    return {
        "message": "Welcome to The Sauce Bottle API",
        "version": "0.1.0",
        "docs": "/api/docs",
        "health": "/api/health",
        "api_v1": "/api/v1",
    }


# Run the application (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
