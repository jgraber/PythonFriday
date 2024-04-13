from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_without_login_gets_401_unauthorized():
    response = client.get("/users/me")
    assert response.status_code == 401


def test_login_with_stanley():
    credentials = {"username": "stanley",
                   "password": "secret"}
    response = client.post("/token", data=credentials)
    assert response.status_code == 200
    jwt = response.json()["access_token"]
    
    print("*" * 50)
    print(jwt)
    print("*" * 50)

    response_me = client.get("/users/me", 
                             headers={"Authorization": "Bearer " + jwt})
    assert response_me.status_code == 200
    assert response_me.json() == {'username': 'stanley', 
                                  'email': 'Stanley.Jobson@localhost', 
                                  'full_name': 'Stanley Jobson', 
                                  'disabled': False}


def test_login_with_mike():
    credentials = {"username": "mike",
                   "password": "password"}
    response = client.post("/token", data=credentials)
    assert response.status_code == 200
    jwt = response.json()["access_token"]
    
    print("*" * 50)
    print(jwt)
    print("*" * 50)
    
    response_me = client.get("/users/me", 
                             headers={"Authorization": "Bearer " + jwt})
    assert response_me.status_code == 200
    assert response_me.json() == {'username': 'mike', 
                                  'email': 'Mike.Doe@localhost', 
                                  'full_name': 'Mike Doe', 
                                  'disabled': False}