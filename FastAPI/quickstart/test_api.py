from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_item():
    response = client.get("/items/5")
    assert response.status_code == 200
    assert response.json() == {'item_id': 5, 'q': None}


def test_read_item_with_querry():
    response = client.get("/items/10?q=abjdljlajlf")
    assert response.status_code == 200
    assert response.json() == {'item_id': 10, 'q': 'abjdljlajlf'}


def test_read_item_wrongly_called():
    response = client.get("/items/rrr")
    assert response.status_code == 422
    answer = response.json()['detail']
    assert answer[0]['msg'] == 'Input should be a valid integer, unable to parse string as an integer'