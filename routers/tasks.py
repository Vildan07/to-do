from fastapi import APIRouter, status, HTTPException, Depends, WebSocket, WebSocketDisconnect, BackgroundTasks
from firebase_admin import messaging
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import asyncio

from models import Tasks, Users
from routers.auth import get_current_user
from utils.utils import send_notification
from schemas.tasks import TasksCreate, TasksUpdate
from schemas.response_schemas import TasksResponse, UsersResponse
from database import get_db
from bots.main import send_telegram_message
from utils.utils import schema_pagination


tasks_router = APIRouter(tags=["Tasks"])


@tasks_router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task: TasksCreate, db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    data = db.query(Tasks).filter(Tasks.title == task.title, Tasks.user_id == current_user.id).first()
    if data:
        raise HTTPException(status_code=400, detail="Task is already in DB!")
    new_task = Tasks(
        title=task.title,
        text=task.text,
        status=task.status,
        user_id=current_user.id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    await send_telegram_message(
        message=f"Task yaraldi!\n{new_task.title}\n{new_task.text}",
        db=db
    )
    users = db.query(Users).all()
    for user in users:
        if user.firebase_token:
            await send_notification(
                title="Task created",
                body=new_task.title,
                token=user.firebase_token
            )

    return {"msg": "Task created", "task_id": new_task.id}


@tasks_router.get("/tasks", status_code=status.HTTP_200_OK)
def read_tasks(page: int = 0, limit: int = 0, task_id: Optional[int] = None, db: Session = Depends(get_db),
               current_user: UsersResponse = Depends(get_current_user)):
    if task_id:
        data = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == current_user.id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Task not found!")
        return TasksResponse.from_orm(data)

    data = db.query(Tasks).filter(Tasks.user_id == current_user.id)

    return schema_pagination(form=data, schema=TasksResponse, limit=limit, page=page)


@tasks_router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task: TasksUpdate, db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    existing_task = db.query(Tasks).filter(Tasks.id == task_id, Tasks.user_id == current_user.id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found or you don't have permission to update it.")

    for key, value in task.model_dump(exclude_unset=True).items():
        if key != "updated_at":
            setattr(existing_task, key, value)

    existing_task.updated_at = datetime.now()

    db.commit()
    db.refresh(existing_task)

    await send_telegram_message(
        message=(f"Task o'zgardi:\nID: {task_id}\nTitle: {existing_task.title}\nText: {existing_task.text}\nUpdated Time: {existing_task.updated_at}"),
        db=db
    )

    users = db.query(Users).all()
    for user in users:
        if user.firebase_token:
            await send_notification(
                title="Task updated",
                body=existing_task.title,
                token=user.firebase_token
            )

    return {"msg": f"Task updated! Task ID: {task_id}"}












