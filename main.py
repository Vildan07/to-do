from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers.users import users_router
from routers.tasks import tasks_router
from routers.bots import bots_router
from routers.auth import auth_router
from routers.firebases import init_firebase

app = FastAPI()

init_firebase()

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(bots_router)
app.include_router(auth_router)
