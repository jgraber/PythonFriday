from datetime import date, timedelta
import logging
import os

from fastapi.testclient import TestClient
import pytest

from ..data.entities import User

from ..dependencies import db_file
from ..main import app

from ..data.database import create_async_session_factory
from ..data.datastore_db import DataStoreDb
from ..authentication import current_active_user, fastapi_users
logging.getLogger("httpx").setLevel(logging.WARNING)


@pytest.fixture(scope="class")
def test_client():
    async def db_file_override():
        db_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            'db',
            'test_db.sqlite')
        return db_file
    app.dependency_overrides[db_file] = db_file_override
    client = TestClient(app)
    yield client


@pytest.mark.asyncio
async def test_create_task_without_authentication_throws_401_error(test_client):
    data = {
        "name": "A first task",
        "priority": 5,
        "due_date": str(date.today() + timedelta(days=1)),
        "done": False
    }

    response = test_client.post("/api/todo/", json=data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_about_me_without_authentication_throws_401_error(test_client):
    response = test_client.get("/about/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_user_can_register(test_client):
    data = {
        "email": "register@example.com",
        "password": "P@ssword123$",
        }
    response = test_client.post("/auth/register", json=data)
    assert response.status_code == 201
    assert response.json()["is_active"] == True
    assert response.json()["is_superuser"] == False
    assert response.json()["is_verified"] == False


@pytest.mark.asyncio
async def test_user_can_login_and_sees_email_in_about_me(test_client):
    data = {
        "email": "check@example.com",
        "password": "P@ssword123$",
        }
    response = test_client.post("/auth/register", json=data)
    assert response.status_code == 201
    print(f"==>'{response.json()}")
    id = response.json()["id"]

    login_data = {
        "username": "check@example.com",
        "password": "P@ssword123$"
        }

    response = test_client.post("/auth/jwt/login", data=login_data)
    response.status_code == 200
    jwt = response.json()["access_token"]
    
    response = test_client.get("/users/me", headers={"Authorization": "Bearer " + jwt})
    response.status_code == 200
    assert response.json()["email"] == "check@example.com" 
    print(response.json())

    response = test_client.get("/about/me", headers={"Authorization": "Bearer " + jwt})
    response.status_code == 200
    assert response.json()["message"] == "Hello check@example.com!" 
    # print(response.json())

