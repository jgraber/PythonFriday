from datetime import date
from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter

from ..data.entities import Task

class TaskFilter(Filter):
    id: Optional[int] = None
    name: Optional[str] = None
    priority: Optional[list[int]] = None
    due_date__lte: Optional[date] = None
    done: Optional[bool] = None
    order_by: list[str] = ["name"]
    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Task
        search_model_fields = ["name"]