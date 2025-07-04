from sqlalchemy import Column, Date, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from backend.app.database import Base


class Politician(Base):
    """SQLAlchemy model for Australian politicians."""

    __tablename__ = "politicians"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    chamber = Column(String, nullable=True)  # e.g., "House of Representatives", "Senate"
    position_title = Column(String, nullable=True)  # e.g. "Minister for Health"
    electorate = Column(String, nullable=True)  # e.g., "Division of Melbourne"
    state = Column(String, nullable=True)  # e.g., "Victoria", "New South Wales"
    date_elected = Column(Date, nullable=True)
    sitting_status = Column(String, nullable=True) # e.g., "Current", "Former", "Candidate"
    is_cabinet_minister = Column(Integer, nullable=True)  # 1 for Yes, 0 for No
    is_shadow_minister = Column(Integer, nullable=True)  # 1 for Yes, 0 for No
    previous_positions = Column(String, nullable=True)  # Comma-separated list of previous positions
    website_url = Column(String, nullable=True)  # URL to the politician's official website
    social_media_links = Column(String, nullable=True)  # JSON or comma-separated links to social media profiles
    statement_count = Column(Integer, default=0)  # Number of statements made by the politician found in db
    tags = Column(String, nullable=True)  # Comma-separated tags for categorization, e.g. climate, health,
    profile_picture_url = Column(String, nullable=True)  # URL to the politician's profile picture
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    statements = relationship("Statement", back_populates="politician")

