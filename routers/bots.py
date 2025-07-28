from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Bots
from routers.auth import get_current_user
from schemas.response_schemas import BotsResponse, UsersResponse
from schemas.bots import BotsCreate, BotsUpdate


bots_router = APIRouter(tags=["Bots"])


@bots_router.post("/bots", status_code=status.HTTP_201_CREATED)
def create_bot(bot: BotsCreate, db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=400, detail="Sizda xuquq yo'q!")
    data = db.query(Bots).first()
    if data:
        raise HTTPException(status_code=400, detail="Bot allaqachon mavjud!")
    data = Bots(token=bot.token, channel_id=bot.channel_id)
    db.add(data)
    db.commit()
    return {"msg": "Bot created!"}


@bots_router.get("/bots", status_code=status.HTTP_200_OK)
def read_bot(db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=400, detail="Sizda xuquq yo'q!")
    data = db.query(Bots).all()
    return data


@bots_router.put("/bots", status_code=status.HTTP_200_OK)
def update_bot(bot: BotsUpdate, db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    if current_user.username != "admin":
        raise HTTPException(status_code=400, detail="Sizda xuquq yo'q!")
    data = db.query(Bots).first()
    if data is None:
        raise HTTPException(status_code=404, detail="Bot not found!")
    for key, value in bot.model_dump().items():
        setattr(data, key, value)
    db.commit()
    db.refresh(data)
    return {"msg": "Bot updated!"}