from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

class UsersResponse(BaseModel):
    id: int
    username: str
    name: str
    phone: str
    firebase_token: Optional[str]

    tasks: List["TasksResponse"] = []

    class Config:
        from_attributes = True


class TasksResponse(BaseModel):
    id: int
    title: str
    text: str
    status: bool
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BotsResponse(BaseModel):
    id: int
    token: str
    channel_id: str