from typing import Annotated, Union
from fastapi import Body, FastAPI, Request, Response
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    a: int
    b: str
    c: bool
    

@app.post("/check")
async def check(item: Item):
    return {"item": item, "result": f"{item.a}-{item.b}"}


@app.post("/check2")
async def check2(a: Annotated[int, Body()], b: Annotated[str, Body()], c: Annotated[bool, Body()]):
    
    return {"item": {"a": a, "b": b, "c": c}, "result": f"{a}-{b}"}
    
