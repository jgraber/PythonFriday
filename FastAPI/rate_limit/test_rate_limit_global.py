from fastapi.testclient import TestClient
from .main_global import app

client = TestClient(app)

def test_limit_global():
    response = client.get("/max/1")
    assert response.status_code == 200

    response = client.get("/max/2")
    assert response.status_code == 200

    response = client.get("/max/3")
    assert response.status_code == 200

    response = client.get("/max/1")
    assert response.status_code == 429
    assert response.json()["error"] == "Rate limit exceeded: 3 per 1 minute"

    response = client.get("/max/4")
    assert response.status_code == 429
    assert response.json()["error"] == "Rate limit exceeded: 3 per 1 minute"

    response = client.get("/hi")
    assert response.status_code == 429
    assert response.json()["error"] == "Rate limit exceeded: 3 per 1 minute"