from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest
from .main import app, Item

client = TestClient(app)


def test_item_model():
    data = {
        "a": 1,
        "b": "b",
        "c": False
    }

    item = Item(**data)
    print(item)
    assert item.a == 1
    assert item.b == "b"
    assert item.c == False


def test_item_model_with_wrong_types():
    data = {
        "a": 1,
        "b": True, # <-- not a string
        "c": False
    }

    with pytest.raises(ValidationError) as info:
        item = Item(**data)
    
    assert "Input should be a valid string" in str(info.value)


def test_send_data():
    data = {
        "a": 13,
        "b": "ABC",
        "c": True
    }

    response = client.post("/check", json=data)
    
    assert response.status_code == 200
    assert response.json()["item"] == data
    assert response.json()["result"] == "13-ABC"


def test_send_data_to_check2():
    data = {
        "a": 13,
        "b": "ABC",
        "c": True
    }

    response = client.post("/check2", json=data)
    
    assert response.status_code == 200
    assert response.json()["item"] == data
    assert response.json()["result"] == "13-ABC"