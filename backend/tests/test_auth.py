from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_register_user(client):
    email = f"{uuid4()}@example.com"
    password = "testpassword123"

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == email
    assert "id" in data


@pytest.mark.skip(reason="Requires isolated async test database")
@pytest.mark.asyncio
async def test_login_user(client):
    email = f"{uuid4()}@example.com"
    password = "testpassword123"

    await client.post(
        "/api/v1/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"