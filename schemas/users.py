from pydantic import BaseModel
from typing import Optional


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class User(BaseModel):
    id: int
    username: str
    firebase_token: str


class UsersCreate(BaseModel):
    username: str
    password: str
    email: str
    name: str
    phone: str


class FirebaseTokenForm(BaseModel):
    firebase_token: str


class UsersUpdate(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]
