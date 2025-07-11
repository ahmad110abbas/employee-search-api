import pytest
from app.db.session import get_db
from app.db.models import Employee

def test_search_employees(client, sample_employee):
    # Add test data
    with next(get_db()) as db:
        db_employee = Employee(**sample_employee)
        db.add(db_employee)
        db.commit()
    
    # Test search
    response = client.post("/api/v1/employees/search", json={})
    assert response.status_code == 200
    assert len(response.json()["results"]) > 0

def test_rate_limiting(client):
    for _ in range(10):
        client.post("/api/v1/employees/search", json={})
    
    # 11th request should be rate limited
    response = client.post("/api/v1/employees/search", json={})
    assert response.status_code == 429

def test_filters(client, sample_employee):
    # Test department filter
    response = client.post("/api/v1/employees/search", json={
        "department": "Testing"
    })
    assert response.status_code == 200
    assert response.json()["results"][0]["department"] == "Testing"

def test_pagination(client):
    response = client.post("/api/v1/employees/search?page=2&size=5", json={})
    assert response.status_code == 200
    pagination = response.json()["pagination"]
    assert pagination["page"] == 2