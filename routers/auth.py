from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm.session import Session

from database import get_db
from models import Users
from schemas.users import Token, TokenData

session = Session()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(tags=["Token"])


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = db.query(Users).filter(Users.token == token).first()
    if user is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username) # -------------------
    except JWTError:
        raise credentials_exception

    user = db.query(Users).where(Users.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.status == 10:
#         return current_user
#     raise HTTPException(status_code=401, detail="Inactive user")


def token_has_expired(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration_time = datetime.fromtimestamp(payload.get("exp"))
        current_time = datetime.utcnow()
        return current_time > expiration_time
    except jwt.JWTError:
        return False


@auth_router.post("/token", response_model=Token)
async def token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(Users).where(Users.username == form_data.username).first() # -------------------
    if user:
        is_validate_password = pwd_context.verify(form_data.password, user.password) # -------------------
    else:
        is_validate_password = False
    if not is_validate_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parolda xatolik",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    db.query(Users).filter(Users.id == user.id).update({
        Users.token: access_token
    })
    db.commit()
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@auth_router.post("/refresh_token", response_model=Token)
async def refresh_token(db: Session = Depends(get_db), token: str = None):
    user = db.query(Users).where(Users.token == token).first()
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Token error",
        )
    # if not token_has_expired(token):
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Token has not expired",
    #     )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    db.query(Users).filter(Users.id == user.id).update({
        Users.token: access_token
    })
    db.commit()
    user = db.query(Users).where(Users.token == access_token).first()
    return {
            "access_token": access_token,
            "token_type": "bearer"
            }


# @auth_router.get("/profile")
# def get_profile(current_user: UserAccessResponse = Depends(get_current_user)):
#     if current_user.role.name != "admin":
#         raise HTTPException(status_code=400, detail="Sizda yetarli huquqlar yo'q")

