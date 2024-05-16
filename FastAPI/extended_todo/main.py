from fastapi import Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .data.datastore_db import DataStoreDb
from .dependencies import get_db
from .routers import todo
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
app.include_router(todo.router, prefix="/api/todo")

app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'static'))), name="static")

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

@app.get("/about", response_class=HTMLResponse)
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
