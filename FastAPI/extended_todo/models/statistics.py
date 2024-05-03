from pydantic import BaseModel

class StatisticOverview(BaseModel):
    total_tasks: int
    total_done: int
    total_open: int