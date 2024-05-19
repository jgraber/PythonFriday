from datetime import date, timedelta
import os
import re
from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
import pytest

from ..dependencies import get_db
from ..data.datastore_db import DataStoreDb
from ..data.database import create_async_session_factory, create_session_factory
from ..main import app

import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

async def override_get_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'db',
        'test_db.sqlite')
    factory = await create_async_session_factory(db_file)
    db = DataStoreDb(factory)
    yield db
    

client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_task():
    data = {
        "name": "A first task",
        "priority": 5,
        "due_date": str(date.today() + timedelta(days=1)),
        "done": False
    }

    response = client.post("/api/todo/", json=data)
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
async def prepare_task(name, priority=4, due_date=None, done=False):
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
async def test_show_task():
    name = "A second task"
    id = await prepare_task(name)

    response = client.get(f"/api/todo/{id}")
    assert response.status_code == 200
    details = response.json()
    assert details['name'] == name


@pytest.mark.asyncio
async def test_show_task_where_task_is_unknown():
    response = client.get(f"/api/todo/-1")
    assert response.status_code == 404
    assert response.json()['detail'] == "Task not found"


@pytest.mark.asyncio
async def test_update_task():
    id = await prepare_task("original")

    update = {
        "name": "An updated task",
        "priority": 5,
        "due_date": str(date.today() + timedelta(days=2)),
        "done": False
    }

    response = client.put(f"/api/todo/{id}", json=update)
    assert response.status_code == 200
    assert response.json()['name'] == "An updated task"

    check = client.get(f"/api/todo/{id}")
    assert check.json()['name'] == "An updated task"


@pytest.mark.asyncio
async def test_delete_task():
    id = await prepare_task("to delete")
    response = client.delete(f"/api/todo/{id}")
    assert response.status_code == 204

    check = client.get(f"/api/todo/{id}")
    assert check.status_code == 404


@pytest.mark.asyncio
async def test_main_page_shows_info_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()['message'] == "The minimalistic ToDo API"


@pytest.mark.asyncio
async def test_show_all_tasks():
    await prepare_task("a first task")
    await prepare_task("a second task")
    await prepare_task("a third task")

    response = client.get("/api/todo")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 3


@pytest.mark.asyncio
async def test_show_all_tasks_that_are_not_done():
    await prepare_task("a finished task", done=True)
    await prepare_task("an open task", done=False)

    response = client.get("/api/todo?include_done=false")

    assert response.status_code == 200
    tasks = response.json()
    done = [task for task in tasks if task['done'] == True]
    assert len(done) == 0


@pytest.mark.asyncio
async def test_show_all_tasks_that_are_due_within_five_days():
    await prepare_task("in 10 days", due_date=date.today() + timedelta(days=10))

    response = client.get(f"/api/todo?due_before={date.today() + timedelta(days=5)}")

    assert response.status_code == 200
    tasks = response.json()
    done = [task for task in tasks if date.fromisoformat(task['due_date']) > date.today() + timedelta(days=5)]
    assert len(done) == 0


@pytest.mark.asyncio
async def test_docs_endpoint_works():
    response = client.get("/openapi.json")
    # No exception -> test passes


@pytest.mark.asyncio
async def test_about_page():
    response = client.get("/about")
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, 'html.parser')
    assert soup.title.text == "About To-Do Task API"
    assert soup.body.h1.text == "About"


@pytest.mark.asyncio
async def test_dashboard():
    response = client.get("/dashboard")
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, 'html.parser')
    assert soup.title.text == "Dashboard To-Do Task API"
    assert soup.body.h1.text == "Dashboard"
    numbers = re.findall(r"\d+", soup.body.p.text)
    assert  int(numbers[0]) == int(numbers[1]) + int(numbers[2])