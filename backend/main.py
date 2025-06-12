from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI applicaiton instance
app = FastAPI(
    title="The Sauce Bottle API",
    description="Australian political statement tracking and analysis.",
    version="0.1.0"
)

# Configure CORS
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
        "message": "Welcome to The Sauce Bottle API.",
        "version": "0.1.0",
        "status": "running",
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "message": "API is running successfully",
    }

# Run the application (for development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
