from typing import Optional
from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str
    status: str


class TaskWithID(Task):
    id: int


class TaskV2(BaseModel):
    title: str
    description: str
    status: str
    priority: Optional[str]


class TaskV2WithID(TaskV2):
    id: int
