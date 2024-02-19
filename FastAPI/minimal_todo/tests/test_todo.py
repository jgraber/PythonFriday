from datetime import date, timedelta
from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_create_task():
    data = {
        "name": "A first task",
        "priority": 5,
        "due_date": str(date.today() + timedelta(days=1))
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


