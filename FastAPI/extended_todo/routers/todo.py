from datetime import date, timedelta
import os
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..data import db_session

from ..models.todo import TaskOutput, TaskInput
from ..data.datastore_db import DataStoreDb

router = APIRouter()

def get_db_file():
    db_file = os.path.join(
            os.path.dirname(__file__),
            '..',
            'db',
            'api.sqlite')
    return db_file

db_session.global_init(get_db_file())
session = db_session.factory()


db = DataStoreDb(session)

async def filter_parameters(q: str | None = None, 
                            include_done: bool = True, 
                            due_before: date = date.today() + timedelta(days=365)):
    return {"q": q, "include_done": include_done, "due_before": due_before }


@router.get("/")
async def show_all_tasks(filter: Annotated[dict, Depends(filter_parameters)]) -> List[TaskOutput]:
    result = db.all()

    if not filter["include_done"]:
        result = [item for item in result if item.done == False ]

    result = [item for item in result if item.due_date <= filter["due_before"] ]

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskInput, request: Request) -> TaskOutput:
    result = db.add(task)
    headers = {"Location": f"{request.base_url}api/todo/{result.id}"}
    return JSONResponse(content=jsonable_encoder(result), 
                        status_code=status.HTTP_201_CREATED,
                        headers=headers)


@router.get("/{id}")
async def show_task(id: int) -> TaskOutput:
    result = db.get(id)

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    

@router.put("/{id}")
async def update_task(id: int, task: TaskInput) -> TaskOutput:
    try:
        result = db.update(id, task)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int) -> None:
    db.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
