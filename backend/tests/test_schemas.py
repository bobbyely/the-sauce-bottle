import pytest
from pydantic import ValidationError
from backend.app.schemas.politician import PoliticianCreate
from backend.app.schemas.statement import Statement, StatementCreate
from datetime import datetime


def test_politician_create_valid():
    data = {"name": "John Doe", "party": "Independent"}
    schema = PoliticianCreate(**data)
    assert schema.name == "John Doe"
    assert schema.party == "Independent"


def test_politician_create_missing_name():
    data = {"party": "Independent"}
    with pytest.raises(ValidationError) as exc_info:
        PoliticianCreate(**data)
    assert "Field required" in str(exc_info.value)


def test_statement_create_valid():
    data = {"content": "This is a statement.", "politician_id": 1}
    schema = StatementCreate(**data)
    assert schema.content == "This is a statement."
    assert schema.politician_id == 1


def test_statement_create_missing_content():
    data = {"politician_id": 1}
    with pytest.raises(ValidationError) as exc_info:
        StatementCreate(**data)
    assert "Field required" in str(exc_info.value)

def test_statement_response_serialization():
    now = datetime.now()
    data = {
        "id": 1,
        "content": "This is a statement.",
        "politician_id": 1,
        "created_at": now,
        "updated_at": now
    }
    schema = Statement(**data)
    assert schema.id == 1
    assert schema.created_at == now

