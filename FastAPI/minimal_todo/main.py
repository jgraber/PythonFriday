from fastapi import FastAPI, HTTPException
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
                        done=task.done, 
                        created_at=date.today())
    db.append(result)
    return result


@app.get("/api/todo/{id}")
async def show_task(id: int):
    result = [item for item in db if item.id == id]
    # return result[0]

    if len(result) > 0:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    


@app.put("/api/todo/{id}")
async def update_task(id: int, task: TaskInput):
    result = [item for item in db if item.id == id]

    if len(result) == 1:
        current = result[0]
        current.name = task.name
        current.priority = task.priority
        current.due_date = task.due_date
        current.done = task.done

        return current
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    

@app.delete("/api/todo/{id}")
async def delete_task(id: int):
    result = [item for item in db if item.id == id]

    if len(result) == 1:
        db.remove(result[0])
