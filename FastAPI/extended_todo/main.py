from fastapi import Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .data.entities import User

from .models.user import UserCreate, UserRead, UserUpdate
from .authentication import auth_backend, current_active_user, fastapi_users

from .data.datastore_db import DataStoreDb
from .dependencies import get_db
from .routers import todo
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

tags_metadata = [
    {
        "name": "auth",
        "description": "Authentication based on FastAPI Users.",
    },
    {
        "name": "users",
        "description": "Basic information about users",
    },
    {
        "name": "tasks",
        "description": "Manage _tasks_ to learn about FastAPI",
        "externalDocs": {
            "description": "Blog series on FastAPI",
            "url": "https://improveandrepeat.com/tag/fastapi/",
        },
    },
]


description = """
## Extended ToDo API

### Topcis covered
- FastAPI
- Routers
- HTML Templates
- Authentication
- Rate limits
- Versioning
"""

app = FastAPI(title="Extended ToDo API",
    description=description,
    summary="An extended example for FastAPI",
    version="0.7.5",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Johnny Graber",
        "url": "https://improveandrepeat.com/about/",
        "email": "info@improveandrepeat.com",
    },
    openapi_tags=tags_metadata,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },)

app.include_router(todo.router, prefix="/api/todo", tags=["tasks"], deprecated=True)
app.include_router(todo.router, prefix="/api/v1/todo", tags=["tasks"])
app.include_router(todo.router, prefix="/api/latest/todo", tags=["tasks"])

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)



@app.get("/about/me", tags=["users"])
async def about_me(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}



app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

@app.get("/about", tags=["users"], response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request, name="about.html"
    )

@app.get("/", include_in_schema=False)
async def main():
    return {'message':'The minimalistic ToDo API'}

# @app.get("/dashboard", include_in_schema=False)
# async def dashboard():
#     return HTMLResponse(content="<html><body><h1>Dashboard</h1>" +
#                         "<p>12 new Task in last 7 days.</p></body></html>")

@app.get("/dashboard", include_in_schema=False)
async def dashboard(request: Request, db: DataStoreDb = Depends(get_db)):
    stats = await db.get_statistics()
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context=jsonable_encoder(stats)
    )
