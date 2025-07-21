from pydantic import BaseModel
from typing import Optional

class BotsCreate(BaseModel):
    token: str
    channel_id: str


class BotsUpdate(BaseModel):
    token: Optional[str] = None
    channel_id: Optional[str] = None
