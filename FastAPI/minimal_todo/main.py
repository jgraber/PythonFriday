from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .models.todo import *
from .data.datastore import DataStore

app = FastAPI()

db = DataStore()

async def filter_parameters(q: str | None = None, 
                            include_done: bool = True, 
                            due_before: date = date.today() + timedelta(days=365)):
    return {"q": q, "include_done": include_done, "due_before": due_before }


@app.get("/")
async def main():
    return {'message':'The minimalistic ToDo API'}


@app.get("/api/todo")
async def show_all_tasks(filter: Annotated[dict, Depends(filter_parameters)]):
    result = db.all()

    if not filter["include_done"]:
        result = [item for item in result if item.done == False ]

    result = [item for item in result if item.due_date <= filter["due_before"] ]

    return result

@app.post("/api/todo")
async def create_task(task: TaskInput, request: Request) -> TaskOutput:
    result = db.add(task)
    headers = {"Location": f"{request.base_url}api/todo/{result.id}"}
    return JSONResponse(content=jsonable_encoder(result), 
                        status_code=status.HTTP_201_CREATED,
                        headers=headers)


@app.get("/api/todo/{id}")
async def show_task(id: int):
    result = db.get(id)

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    


@app.put("/api/todo/{id}")
async def update_task(id: int, task: TaskInput):
    try:
        result = db.update(id, task)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
    

@app.delete("/api/todo/{id}")
async def delete_task(id: int):
    db.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
