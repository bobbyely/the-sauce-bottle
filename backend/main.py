from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from backend.app.api.api import api_router
from backend.app.api.endpoints.health import router as health_router
from backend.app.core.exceptions import SauceBottleException
from backend.app.schemas.error import ErrorResponse, ValidationErrorResponse, ErrorDetail

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

# Exception handlers
@app.exception_handler(SauceBottleException)
async def sauce_bottle_exception_handler(request: Request, exc: SauceBottleException):
    """Handle custom SauceBottle exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.message,
            details=[ErrorDetail(message=str(v), field=k) for k, v in exc.details.items()] if exc.details else None,
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="HTTPException",
            message=str(exc.detail),
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        details.append(ErrorDetail(
            field=field,
            message=error["msg"],
            code=error["type"]
        ))
    
    return JSONResponse(
        status_code=422,
        content=ValidationErrorResponse(
            details=details,
            status_code=422
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred. Please try again later.",
            status_code=500
        ).model_dump()
    )

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
