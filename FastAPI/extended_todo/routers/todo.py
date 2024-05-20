from datetime import date, timedelta
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..dependencies import get_db

from ..models.todo import TaskOutput, TaskInput
from ..data.datastore_db import DataStoreDb

router = APIRouter()


async def filter_parameters(q: str | None = None, 
                            include_done: bool = True, 
                            due_before: date = date.today() + timedelta(days=365)):
    return {"q": q, "include_done": include_done, "due_before": due_before }


@router.get("/")
async def show_all_tasks(filter: Annotated[dict, Depends(filter_parameters)], 
                         db: DataStoreDb = Depends(get_db)) -> List[TaskOutput]:
    result = await db.all()

    if not filter["include_done"]:
        result = [item for item in result if item.done == False ]

    result = [item for item in result if item.due_date <= filter["due_before"] ]

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskInput, 
                      request: Request, 
                      db: DataStoreDb = Depends(get_db)) -> TaskOutput:
    result = await db.add(task)
    headers = {"Location": f"{request.base_url}api/todo/{result.id}"}
    return JSONResponse(content=jsonable_encoder(result), 
                        status_code=status.HTTP_201_CREATED,
                        headers=headers)


@router.get("/{id}")
async def show_task(id: int, 
                    db: DataStoreDb = Depends(get_db)) -> TaskOutput:
    result = await db.get(id)

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    

@router.put("/{id}")
async def update_task(id: int, 
                      task: TaskInput, 
                      db: DataStoreDb = Depends(get_db)) -> TaskOutput:
    try:
        result = await db.update(id, task)
        return result
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int, 
                      db: DataStoreDb = Depends(get_db)) -> None:
    await db.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
