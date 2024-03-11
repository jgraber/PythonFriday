from datetime import date, timedelta
from typing import Annotated
from pydantic import BaseModel, Field, field_validator

class TaskInput(BaseModel):
    name: str = Field(str, min_length=5, max_length=100)
    priority: int = Field(gt=0, lt=10)
    # due_date: date = Field(ge=date.today(), le=date.today() + timedelta(days=365))
    due_date: date
    done: bool

    @field_validator('due_date')
    def due_date_must_be_between_today_and_one_year_in_the_future(cls, v):
        if not date.today() <= v <= date.today() + timedelta(days=365):
            raise ValueError("due_date must be between today and one year in the future")
        return v

class TaskOutput(BaseModel):
    id: int
    name: str
    priority: int
    due_date: date
    done: bool
    created_at: date