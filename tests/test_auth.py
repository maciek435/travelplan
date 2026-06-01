import pytest

async def test_register_user(client):
    response = await client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "haslo123"
    })

    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"

async def test_login(client):
    await client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "haslo123"
    })
    
    response = await client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "haslo123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()

async def test_wrong_password(client):
    await client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "haslo123"
    })
    
    response = await client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "haslo"
    })

    assert response.status_code == 401