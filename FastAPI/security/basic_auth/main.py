# Example from https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
# extended with a second user, a users dictionary and BCrypt

from typing import Annotated

import bcrypt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

users = {
    "stanley" : {
        "first_name": "Stanley",
        "last_name": "Jobson",
        "password_hash": b'$2b$12$HIbxs5kbjinDEUzbQJYqpeTp.GxRgy4m8hdQM4JnSunGQ6VaY5Ld6', # secret
    },
    "mike" : {
        "first_name": "Mike",
        "last_name": "Doe",
        "password_hash": b'$2b$12$JAM3vz8gEZDeNSDAILiaReTmvoNM5EEP33Elhq5fCoTgno4SxfqKO', # password
    }
}

security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    
    if credentials.username in users:
        user = users[credentials.username]
        pw_hash = user["password_hash"]
    else:
        user = users[max(users.keys())] # only done to get same runtime
        pw_hash = b'$2b$12$bpKSBbvimpx3M357O0Oq8.MMquDtXS/e8jHU4X.tyzQl/qmnKH5uS'
    
    if not (bcrypt.checkpw(credentials.password.encode("utf-8"), pw_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    details = users[username]
    return {"user": username,
            "firstName": details["first_name"],
            "lastName": details["last_name"],
            }