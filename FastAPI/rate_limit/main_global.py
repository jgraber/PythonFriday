from datetime import datetime
from fastapi import FastAPI, Request

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


limiter = Limiter(key_func=get_remote_address, application_limits=["3/minute"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.get("/max/{id}")
async def myendpoint(request: Request, id: int):
    return {"id":id, "viewed":datetime.now()}


@app.get("/hi")
async def hello(request: Request):
    return {"message": "Hello"}