import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import Base, engine, SessionLocal
from app.models import Employee

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    return TestClient(app)

@pytest.fixture
def sample_employee():
    return {
        "first_name": "Test",
        "last_name": "User",
        "contact_info": "test@example.com",
        "department": "Testing",
        "position": "QA",
        "location": "Test City",
        "status": "active"
    }