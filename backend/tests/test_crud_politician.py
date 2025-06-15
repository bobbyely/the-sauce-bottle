import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.models.politician import Politician, Base
from backend.app.schemas.politician import PoliticianCreate, PoliticianUpdate
from backend.app.crud import politician

# Setup an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    """Create a new database session for a test."""
    Base.metadata.create_all(bind=engine)  # Create tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_and_get_politician(db):
    """Test creating and retrieving a politician."""
    # Create
    pol_in = PoliticianCreate(name="Test Name")
    pol = politician.create(db, pol_in)
    assert pol.id is not None
    assert pol.name == "Test Name"

    # Get
    fetched = politician.get(db, pol.id)
    assert fetched is not None
    assert fetched.name == "Test Name"

def test_update_politician(db):
    """Test updating a politician."""
    # Create
    pol_in = PoliticianCreate(name="Initial Name")
    pol = politician.create(db, pol_in)

    # Update
    update_data = PoliticianUpdate(name="Updated Name", party="Test Party")
    updated_pol = politician.update(db, pol, update_data)
    assert updated_pol.name == "Updated Name"
    assert updated_pol.party == "Test Party"

    # Ensure the original object is updated
    fetched = politician.get(db, pol.id)
    assert fetched.name == "Updated Name"
    assert fetched.party == "Test Party"



def test_remove_politician(db):
    """Test removing a politician."""
    # Create
    pol_in = PoliticianCreate(name="To Be Removed")
    pol = politician.create(db, pol_in)
    # Remove
    removed = politician.remove(db, pol.id)
    assert removed is not None
    # Ensure its gone
    assert politician.get(db, pol.id) is None