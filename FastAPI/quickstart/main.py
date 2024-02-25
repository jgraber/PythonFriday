from typing import Union
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/echo")
async def echo(request: Request):
    return request.query_params


# @app.get("/calculator")
# async def calculate(a, b, c):
#     return {"value": a + b + c}


# @app.get("/calculator")
# async def calculate(a, b, c):
#     a = int(a)
#     b = int(b)
#     c = int(c)
#     return {"value": a + b + c}

@app.get("/calculator")
async def calculate(a: int, b: int, c: int):
    return {"value": a + b + c}


# @app.get("/weather/{city}")
# async def weather(city):
#     return {"city": city}

@app.get("/weather/{city}")
async def weather(city: int):
    return {"city": city}


# Installation: pip install fastapi && pip install "uvicorn[standard]"
# Start: uvicorn main:app --reload
# Endpoints:
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/items/1?q=Apples
# http://127.0.0.1:8000/docs