"""Integration tests for authentication endpoints"""
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_and_login_user():
    """Test user registration and login flow"""
    # Use a random email each time so tests don't fail from "email already exists"
    random_email = f"test_{uuid.uuid4().hex}@example.com"
    password = "password123"
    name = "Pytest User"

    # 1. Register
    register_res = client.post(
        "/auth/register",
        json={
            "email": random_email,
            "password": password,
            "name": name
        },
    )

    # Should return 201 (created)
    assert register_res.status_code == 201
    register_data = register_res.json()
    assert register_data["email"] == random_email
    assert register_data["name"] == name
    assert "id" in register_data

    # 2. Login with same credentials
    login_res = client.post(
        "/auth/login",
        json={
            "email": random_email,
            "password": password,
        },
    )

    assert login_res.status_code == 200
    login_data = login_res.json()
    assert login_data["email"] == random_email
    assert "id" in login_data


def test_register_duplicate_email():
    """Test that registering with duplicate email fails"""
    random_email = f"duplicate_{uuid.uuid4().hex}@example.com"
    password = "password123"
    name = "First User"

    # First registration should succeed
    register_res1 = client.post(
        "/auth/register",
        json={
            "email": random_email,
            "password": password,
            "name": name
        },
    )
    assert register_res1.status_code == 201

    # Second registration with same email should fail
    register_res2 = client.post(
        "/auth/register",
        json={
            "email": random_email,
            "password": password,
            "name": "Second User"
        },
    )
    assert register_res2.status_code in [400, 409]  # Bad request or conflict


def test_login_invalid_credentials():
    """Test that login fails with invalid credentials"""
    login_res = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword",
        },
    )
    assert login_res.status_code in [401, 404]  # Unauthorized or not found
