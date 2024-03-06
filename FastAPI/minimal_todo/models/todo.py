from datetime import date, timedelta
from typing import Annotated
from pydantic import BaseModel, Field

class TaskInput(BaseModel):
    name: str = Field(str, min_length=5, max_length=100)
    priority: int = Field(gt=0, lt=10)
    due_date: date = Field(ge=date.today(), le=date.today() + timedelta(days=365))
    done: bool


class TaskOutput(BaseModel):
    id: int
    name: str
    priority: int
    due_date: date
    done: bool
    created_at: date