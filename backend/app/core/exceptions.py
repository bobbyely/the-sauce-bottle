"""Custom exceptions for business logic errors."""
from typing import Optional


class SauceBottleException(Exception):
    """Base exception for The Sauce Bottle application."""
    
    def __init__(self, message: str, status_code: int = 500, details: Optional[dict] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class PoliticianNotFoundError(SauceBottleException):
    """Raised when a politician is not found."""
    
    def __init__(self, politician_id: int):
        super().__init__(
            message=f"Politician with id {politician_id} not found",
            status_code=404,
            details={"politician_id": politician_id}
        )


class StatementNotFoundError(SauceBottleException):
    """Raised when a statement is not found."""
    
    def __init__(self, statement_id: int):
        super().__init__(
            message=f"Statement with id {statement_id} not found",
            status_code=404,
            details={"statement_id": statement_id}
        )


class DuplicatePoliticianError(SauceBottleException):
    """Raised when attempting to create a politician that already exists."""
    
    def __init__(self, name: str):
        super().__init__(
            message=f"Politician with name '{name}' already exists",
            status_code=409,
            details={"politician_name": name}
        )


class DatabaseConnectionError(SauceBottleException):
    """Raised when database connection fails."""
    
    def __init__(self):
        super().__init__(
            message="Unable to connect to database",
            status_code=503,
            details={"service": "database"}
        )


class InvalidDateRangeError(SauceBottleException):
    """Raised when date range parameters are invalid."""
    
    def __init__(self, date_from: str, date_to: str):
        super().__init__(
            message=f"Invalid date range: {date_from} to {date_to}",
            status_code=400,
            details={"date_from": date_from, "date_to": date_to}
        )