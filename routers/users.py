from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models import Users, Tasks
from routers.auth import get_password_hash, get_current_user
from schemas.users import UsersCreate, UsersUpdate
from schemas.response_schemas import UsersResponse
from utils.utils import schema_pagination


users_router = APIRouter(tags=["Users"])


@users_router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UsersCreate, db: Session = Depends(get_db)):
    data = db.query(Users).filter(Users.username == user.username).first()
    if data:
        HTTPException(status_code=400, detail="User with this Username already exist!")
    data = Users(
        username=user.username,
        password=get_password_hash(user.password),
        name=user.name,
        phone=user.phone,
        firebase_token=user.firebase_token
    )
    db.add(data)
    db.commit()
    return {"msg": "User successful created!"}


@users_router.get("/users", response_model=UsersResponse, status_code=status.HTTP_200_OK)
def read_users(db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    data = db.query(Users).filter(Users.id == current_user.id).first()
    if not data:
        raise HTTPException(status_code=403, detail="Siz faqat o'zingizni ma'lumotlaringizni ko'rishingiz mumkun!")
    return data


@users_router.put("/users", status_code=status.HTTP_200_OK)
def update_user(user: UsersUpdate, db: Session = Depends(get_db),
                current_user: UsersResponse = Depends(get_current_user)):
    if current_user.username != user.username:
        raise HTTPException(status_code=403, detail="Siz faqat o'zingizni ma'lumotlaringizni yangilashiz mumkun!")

    data = db.query(Users).filter(Users.username == user.username).first()
    if not data:
        raise HTTPException(status_code=404, detail="User not found!")

    update_data = user.model_dump()
    if "password" in update_data and update_data["password"]:
        update_data["password"] = get_password_hash(update_data["password"])

    for key, value in update_data.items():
        setattr(data, key, value)

    db.commit()
    db.refresh(data)
    return {"msg": "User successful updated!"}

