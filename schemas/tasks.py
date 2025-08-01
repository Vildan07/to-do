from pydantic import BaseModel
from typing import Optional


class TasksCreate(BaseModel):
    title: str
    text: str
    status: bool = False


class TasksUpdate(BaseModel):
    title: Optional[str]
    text: Optional[str]
    status: Optional[bool] = None
