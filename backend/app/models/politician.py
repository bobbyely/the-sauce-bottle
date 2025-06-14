from sqlalchemy import Column, Integer, String

from backend.app.database import Base


class Politician(Base):
    """SQLAlchemy model for Australian politicians."""

    __tablename__ = "politicians"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    party = Column(String, nullable=True)
    position = Column(String, nullable=True)
    # Add more fields as needed
