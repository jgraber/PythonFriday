from fastapi import FastAPI
from .models.todo import *

app = FastAPI()


@app.post("/api/todo")
async def create_task(task: TaskInput):
    pos = 1
    result = TaskOutput(id=pos, 
                        name=task.name, 
                        priority=task.priority, 
                        due_date=task.due_date,
                        done=False, 
                        created_at=date.today())
    return result
