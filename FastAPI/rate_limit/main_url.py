from datetime import datetime
from fastapi import FastAPI, Request

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address) #key_style="endpoint"
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/max/{id}")
@limiter.limit("3/minute")
async def myendpoint(request: Request, id: int):
    return {"id":id, "viewed":datetime.now()}