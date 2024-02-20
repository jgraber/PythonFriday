from datetime import date
from pydantic import BaseModel

class TaskInput(BaseModel):
    name: str
    priority: int
    due_date: date


class TaskOutput(BaseModel):
    id: int
    name: str
    priority: int
    due_date: date
    done: bool
    created_at: date