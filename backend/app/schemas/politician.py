"""Schema for Politician."""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class PoliticianBase(BaseModel):
    name: str
    party: Optional[str] = None
    chamber: Optional[str] = None
    position_title: Optional[str] = None
    electorate: Optional[str] = None
    state: Optional[str] = None
    date_elected: Optional[date] = None
    sitting_status: Optional[str] = None
    is_cabient_minister: Optional[int] = None
    is_shadow_minister: Optional[int] = None
    previous_positions: Optional[str] = None
    website: Optional[str] = None
    social_media_links: Optional[str] = None
    statement_count: Optional[int] = 0
    tags: Optional[str] = None
    profile_picture_url: Optional[str] = None

class PoliticianCreate(PoliticianBase):
    name: str  # Required for creation

class PoliticianUpdate(PoliticianBase):
    name: Optional[str] = None  # all fields optional for update patch/put
    party: Optional[str] = None
    chamber: Optional[str] = None
    position_title: Optional[str] = None
    electorate: Optional[str] = None
    state: Optional[str] = None
    date_elected: Optional[date] = None
    sitting_status: Optional[str] = None
    is_cabient_minister: Optional[int] = None
    is_shadow_minister: Optional[int] = None
    previous_positions: Optional[str] = None
    website: Optional[str] = None
    social_media_links: Optional[str] = None
    statement_count: Optional[int] = 0
    tags: Optional[str] = None
    profile_picture_url: Optional[str] = None

class Politician(PoliticianBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
