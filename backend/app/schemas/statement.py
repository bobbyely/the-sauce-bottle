from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class StatementBase(BaseModel):
    content: str
    date_made: Optional[date] = None
    ai_summary: Optional[str] = None
    ai_contradiction_analysis: Optional[str] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None
    source_name: Optional[str] = None
    review_status: Optional[str] = None

class StatementCreate(StatementBase):
    content: str
    politician_id: int = Field(..., description="ID of the politician who made the statement")

class StatementUpdate(BaseModel):
    content: Optional[str] = None
    date_made: Optional[date] = None
    ai_summary: Optional[str] = None
    ai_contradiction_analysis: Optional[str] = None
    source_url: Optional[str] = None
    source_type: Optional[str] = None
    source_name: Optional[str] = None
    review_status: Optional[str] = None
    politician_id: Optional[int] = None

class Statement(StatementBase):
    id: int
    politician_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
