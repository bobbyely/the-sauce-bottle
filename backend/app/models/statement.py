from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from backend.app.database import Base


class Statement(Base):
    """
    SQLAlchemy model for a political statement.

    Links to a Politician and stores AI Analysis results.
    """

    __tablename__ = "statements"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # The main text of the statement
    date_made = Column(Date, nullable=True)  # Date the statement was made
    politician_id = Column(Integer, ForeignKey("politicians.id"), nullable=False)
    ai_summary = Column(Text, nullable=True)  # AI-generated summary of the statement
    ai_contradiction_analysis = Column(Text, nullable=True)  # AI analysis of contradictions
    source_url = Column(String(1024), nullable=True)  # URL to the statement source
    source_type = Column(String(50), nullable=True)  # Type of source (e.g., "speech", "interview", "public_statement")
    source_name = Column(String(255), nullable=True)  # Name of the source (e.g. ABC News)
    review_status = Column(String(50), default="pending")  # Status of AI review
    created_at = Column(DateTime, server_default=func.current_timestamp())  # Timestamp of creation
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())  # Timestamp of last update
    
    politician = relationship("Politician", back_populates="statements")
