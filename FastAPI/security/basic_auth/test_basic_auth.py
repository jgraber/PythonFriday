import base64
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_without_login_gets_401_unauthorized():
    response = client.get("/users/me")
    assert response.status_code == 401


def test_can_access_endpoint_after_login():
    credentials = base64.b64encode(b"stanley:secret").decode("utf-8")
    response = client.get("/users/me", 
                          headers={"Authorization": "Basic " + credentials})
    assert response.status_code == 200
    assert response.json() == {'firstName': 'Stanley', 
                               'lastName': 'Jobson', 
                               'user': 'stanley'}
    

def test_wrong_password_gives_error():
    credentials = base64.b64encode(b"stanley:password").decode("utf-8")
    response = client.get("/users/me", 
                          headers={"Authorization": "Basic " + credentials})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_wrong_username_gives_error():
    credentials = base64.b64encode(b"MMike:password").decode("utf-8")
    response = client.get("/users/me", 
                          headers={"Authorization": "Basic " + credentials})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

# pytest --durations=0 .\test_basic_auth.py
# 0.22s call     test_basic_auth.py::test_can_access_endpoint_after_login
# 0.22s call     test_basic_auth.py::test_wrong_password_gives_error
# 0.22s call     test_basic_auth.py::test_wrong_username_gives_error
