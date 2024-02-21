from fastapi import FastAPI
from .models.todo import *

app = FastAPI()

db = []

@app.post("/api/todo")
async def create_task(task: TaskInput):
    pos = len(db) + 1
    result = TaskOutput(id=pos, 
                        name=task.name, 
                        priority=task.priority, 
                        due_date=task.due_date,
                        done=False, 
                        created_at=date.today())
    db.append(result)
    return result


@app.get("/api/todo/{id}")
async def show_task(id: int):
    result = [item for item in db if item.id == id]
    return result[0]

