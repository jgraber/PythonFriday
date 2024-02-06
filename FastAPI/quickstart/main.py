from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Installation: pip install fastapi && pip install "uvicorn[standard]"
# Start: uvicorn main:app --reload
# Endpoints:
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/items/1?q=Apples
# http://127.0.0.1:8000/docs