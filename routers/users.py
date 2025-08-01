from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Users, Tasks
from routers.auth import get_password_hash, get_current_user
from schemas.users import UsersCreate, UsersUpdate, FirebaseTokenForm
from schemas.response_schemas import UsersResponse
from utils.utils import send_notification

users_router = APIRouter(tags=["Users"])


@users_router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UsersCreate, db: Session = Depends(get_db)):
    data = db.query(Users).filter(Users.username == user.username).first()
    if data:
        HTTPException(status_code=400, detail="User with this Username already exist!")
    data = Users(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
        name=user.name,
        phone=user.phone,
    )
    db.add(data)
    db.commit()
    return {"msg": "User successful created!"}


@users_router.put("/firebase_token", status_code=200)
def firebase_token(form: FirebaseTokenForm, db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    db.query(Users).filter(Users.id == current_user.id).update({"firebase_token": form.firebase_token})
    db.commit()
    return {"msg": "Firebase Token Created!"}


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


@users_router.post("/users_notification", status_code=201)
async def users_notification(title: str, body: str, db: Session = Depends(get_db),
                             current_user: UsersResponse = Depends(get_current_user)):
    users = db.query(Users.firebase_token).all()
    tokens = [token[0] for token in users if token[0]]
    if not tokens:
        raise HTTPException(status_code=404, detail="Firebase tokenli foydalanuvchilar yoq!")
    for token in tokens:
        try:
            await send_notification(title=title, body=body, token=token)
        except Exception as e:
            print(f"Token yuborishda xatolik {token}: {str(e)}")

    return {"msg": f"Xabarlar {len(tokens)} tadan"}