from datetime import date, timedelta
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_create_task():
    data = {
        "name": "A first task",
        "priority": 5,
        "due_date": str(date.today() + timedelta(days=1)),
        "done": False
    }

    response = client.post("/api/todo/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result['id'] > 0
    assert result['done'] == False
    assert result['created_at'] == str(date.today())
    assert result['name'] == data['name']
    assert result['priority'] == data['priority']
    assert result['due_date'] == data['due_date']


def prepare_task(name, priority=4, due_date=None, done=False):
    data = {
        "name": name,
        "priority": priority,
        "due_date": str(date.today() + timedelta(days=1)),
        "done": done
    }

    prepare_response = client.post("/api/todo/", json=data)
    assert prepare_response.status_code == 200
    return prepare_response.json()['id']

def test_show_task():
    name = "A second task"
    id = prepare_task(name)

    response = client.get(f"/api/todo/{id}")
    assert response.status_code == 200
    details = response.json()
    assert details['name'] == name


def test_show_task_where_task_is_unknown():
    response = client.get(f"/api/todo/-1")
    assert response.status_code == 404
    assert response.json()['detail'] == "Task not found"


def test_update_task():
    id = prepare_task("original")

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


def test_delete_task():
    id = prepare_task("to delete")
    response = client.delete(f"/api/todo/{id}")
    assert response.status_code == 200

    check = client.get(f"/api/todo/{id}")
    assert check.status_code == 404


def test_main_page_shows_info_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()['message'] == "The minimalistic ToDo API"


def test_show_all_tasks():
    prepare_task("a first task")
    prepare_task("a second task")
    prepare_task("a third task")

    response = client.get("/api/todo")

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 3

