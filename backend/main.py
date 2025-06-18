from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.endpoints import politicians
from backend.app.api.health import router as health_router

# Create FastAPI applicaiton instance
app = FastAPI(
    title="The Sauce Bottle API",
    description="Australian political statement tracking and analysis.",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Vue.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# health endpoints
app.include_router(health_router)

# politicians endpoints
app.include_router(politicians.router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning basic API information."""
    return {
        "message": "Welcome to The Sauce Bottle API.",
        "version": "0.1.0",
        "status": "running",
    }



# Run the application (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
