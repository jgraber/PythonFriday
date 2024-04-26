from datetime import date, timedelta
from typing import Annotated
from pydantic import BaseModel, Field, field_validator


class TaskInput(BaseModel):
    name: str
    priority: int = Field(gt=0, lt=10)
    due_date: date
    done: bool

    @field_validator('due_date')
    def due_date_must_be_between_today_and_one_year_in_the_future(cls, v):
        if not date.today() <= v <= date.today() + timedelta(days=365):
            raise ValueError("due_date must be between today and one year in the future")
        return v
    
    @field_validator('name')
    def name_must_be_between_5_and_100(cls, v):
        if len(v) < 5 :
            raise ValueError("String should have at least 5 characters")
        if len(v) > 100:
            raise ValueError("String should have at most 100 characters")
        return v


class TaskOutput(BaseModel):
    id: int
    name: str
    priority: int
    due_date: date
    done: bool
    created_at: date

    class ConfigDict:
        from_attributes = True

