from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routers import todo


app = FastAPI()
app.include_router(todo.router, prefix="/api/todo")


@app.get("/", include_in_schema=False)
async def main():
    return {'message':'The minimalistic ToDo API'}

@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    return HTMLResponse(content="<html><body><h1>Dashboard</h1><p>12 new Task in last 7 days.</p></body></html>")