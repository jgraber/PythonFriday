from datetime import date, timedelta
import os
import re
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
import pytest

from ..data.entities import User

from ..dependencies import get_db, db_file
from ..data.datastore_db import DataStoreDb
from ..data.database import create_async_session_factory
from ..main import app
from ..authentication import current_active_user

import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

test_user = User(email="test@email.com", hashed_password="aaa")

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
    app.dependency_overrides[current_active_user] = lambda: test_user
    client = TestClient(app)
    yield client


@pytest.mark.asyncio
async def test_create_task(test_client):
    data = {
        "name": "A first task",
        "priority": 5,
        "due_date": str(date.today() + timedelta(days=1)),
        "done": False
    }

    response = test_client.post("/api/todo/", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result['id'] > 0
    assert result['done'] == False
    assert result['created_at'] == str(date.today())
    assert result['name'] == data['name']
    assert result['priority'] == data['priority']
    assert result['due_date'] == data['due_date']
    assert f"http://testserver/api/todo/{result['id']}" == response.headers['location']


@pytest.mark.asyncio
async def prepare_task(client, name, priority=4, due_date=None, done=False):
    if due_date == None:
        due_date = date.today() + timedelta(days=1)
    
    data = {
        "name": name,
        "priority": priority,
        "due_date": str(due_date),
        "done": done
    }

    prepare_response = client.post("/api/todo/", json=data)
    assert prepare_response.status_code == 201
    return prepare_response.json()['id']


@pytest.mark.asyncio
async def test_show_task(test_client):
    name = "A second task"
    id = await prepare_task(test_client, name)

    response = test_client.get(f"/api/todo/{id}")
    assert response.status_code == 200
    details = response.json()
    assert details['name'] == name


@pytest.mark.asyncio
async def test_show_task_where_task_is_unknown(test_client):
    response = test_client.get(f"/api/todo/-1")
    assert response.status_code == 404
    assert response.json()['detail'] == "Task not found"


@pytest.mark.asyncio
async def test_update_task(test_client):
    id = await prepare_task(test_client, "original")

    update = {
        "name": "An updated task",
        "priority": 5,
        "due_date": str(date.today() + timedelta(days=2)),
        "done": False
    }

    response = test_client.put(f"/api/todo/{id}", json=update)
    assert response.status_code == 200
    assert response.json()['name'] == "An updated task"

    check = test_client.get(f"/api/todo/{id}")
    assert check.json()['name'] == "An updated task"


@pytest.mark.asyncio
async def test_delete_task(test_client):
    id = await prepare_task(test_client, "to delete")
    response = test_client.delete(f"/api/todo/{id}")
    assert response.status_code == 204

    check = test_client.get(f"/api/todo/{id}")
    assert check.status_code == 404


@pytest.mark.asyncio
async def test_main_page_shows_info_message(test_client):
    response = test_client.get("/")

    assert response.status_code == 200
    assert response.json()['message'] == "The minimalistic ToDo API"


@pytest.mark.asyncio
async def test_show_all_tasks(test_client):
    await prepare_task(test_client, "a first task")
    await prepare_task(test_client, "a second task")
    await prepare_task(test_client, "a third task")

    response = test_client.get("/api/todo")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 3


@pytest.mark.asyncio
async def test_show_all_tasks_that_are_not_done(test_client):
    await prepare_task(test_client, "a finished task", done=True)
    await prepare_task(test_client, "an open task", done=False)

    response = test_client.get("/api/todo?done=false")

    assert response.status_code == 200
    tasks = response.json()
    done = [task for task in tasks if task['done'] == True]
    assert len(done) == 0


@pytest.mark.asyncio
async def test_show_all_tasks_that_are_due_within_five_days(test_client):
    await prepare_task(test_client, "in 10 days", due_date=date.today() + timedelta(days=10))
    await prepare_task(test_client, "in 4 days", due_date=date.today() + timedelta(days=4))

    response = test_client.get(f"/api/todo?done=false&due_date__lte={date.today() + timedelta(days=5)}")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 1
    larger = [task for task in tasks if date.fromisoformat(task['due_date']) > date.today() + timedelta(days=5)]
    assert len(larger) == 0


@pytest.mark.asyncio
async def test_show_all_tasks_that_match_search_criteria_sorted_by_name(test_client):
    await prepare_task(test_client, "485960 A", due_date=date.today())
    await prepare_task(test_client, "485960 B", due_date=date.today())
    await prepare_task(test_client, "485960 C", due_date=date.today())

    response = test_client.get(f"/api/todo?search=485960")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3
    assert tasks[0]["name"] == "485960 A"
    assert tasks[1]["name"] == "485960 B"
    assert tasks[2]["name"] == "485960 C"


@pytest.mark.asyncio
async def test_show_all_tasks_that_match_search_criteria_sorted_by_name_descending(test_client):
    await prepare_task(test_client, "5780383 A", due_date=date.today())
    await prepare_task(test_client, "5780383 B", due_date=date.today())
    await prepare_task(test_client, "5780383 C", due_date=date.today())

    response = test_client.get(f"/api/todo?search=5780383&order_by=-name")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 3
    assert tasks[0]["name"] == "5780383 C"
    assert tasks[1]["name"] == "5780383 B"
    assert tasks[2]["name"] == "5780383 A"


@pytest.mark.asyncio
async def test_docs_endpoint_works(test_client):
    response = test_client.get("/openapi.json")
    # No exception -> test passes


@pytest.mark.asyncio
async def test_about_page(test_client):
    response = test_client.get("/about")
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, 'html.parser')
    assert soup.title.text == "About To-Do Task API"
    assert soup.body.h1.text == "About"


@pytest.mark.asyncio
async def test_dashboard(test_client):
    response = test_client.get("/dashboard")
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, 'html.parser')
    assert soup.title.text == "Dashboard To-Do Task API"
    assert soup.body.h1.text == "Dashboard"
    numbers = re.findall(r"\d+", soup.body.p.text)
    assert  int(numbers[0]) == int(numbers[1]) + int(numbers[2])


@pytest.mark.asyncio
async def test_abount_me(test_client):
    response = test_client.get("/about/me")
    assert response.status_code == 200
    assert test_user.email in response.text