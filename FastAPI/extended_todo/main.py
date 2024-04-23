from fastapi import FastAPI
from .routers import todo


app = FastAPI()
app.include_router(todo.router, prefix="/api/todo")


@app.get("/", include_in_schema=False)
async def main():
    return {'message':'The minimalistic ToDo API'}

