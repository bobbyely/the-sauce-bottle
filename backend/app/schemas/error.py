"""Error response schemas for consistent API error handling."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Individual error detail."""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    status_code: int


class ValidationErrorResponse(BaseModel):
    """Validation error response format."""
    error: str = "Validation Error"
    message: str = "The request contains invalid data"
    details: List[ErrorDetail]
    status_code: int = 422