import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/api/auth/login",
        data={"username": "admin@panchayatguard.gov.in", "password": "SecurePassword123!"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure():
    response = client.post(
        "/api/auth/login",
        data={"username": "admin@panchayatguard.gov.in", "password": "WrongPassword!"}
    )
    assert response.status_code == 401

def test_get_dashboard_unauthorized():
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 401

def test_get_dashboard_authorized():
    # Login first
    login_res = client.post(
        "/api/auth/login",
        data={"username": "admin@panchayatguard.gov.in", "password": "SecurePassword123!"}
    )
    token = login_res.json()["access_token"]
    
    # Get dashboard
    response = client.get(
        "/api/dashboard/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_procurement" in data
    assert "transactions_analyzed" in data
