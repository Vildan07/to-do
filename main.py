from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers.users import users_router
from routers.tasks import tasks_router
from routers.bots import bots_router
from routers.auth import auth_router
from routers.firebases import firebase_router


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(firebase_router)
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(bots_router)
app.include_router(auth_router)


# from typing import Annotated

# from fastapi import FastAPI, File, Form, UploadFile
#
# app = FastAPI()


# @app.post("/files/", deprecated=True)
# async def create_file(
#     file: Annotated[bytes, File()],
#     fileb: Annotated[UploadFile, File()],
#     token: Annotated[str, Form()],
# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }