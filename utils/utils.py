import math
from datetime import datetime
from io import BytesIO

from fastapi import HTTPException, Depends
from firebase_admin import messaging
from sqlalchemy.orm import Session
from openpyxl import load_workbook
import pandas as pd

from models import Tasks
from routers.auth import get_current_user
from database import get_db
from schemas.response_schemas import UsersResponse


def pagination(form, page, limit):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page and limit must be positive integers!")
    elif page and limit:
        return {
            "current_page": page,
            "limit": limit,
            "pages": math.ceil(form.count() / limit),
            "data": form.offset((page - 1) * limit).limit(limit).all()
            }
    else:
        return form.all()


def schema_pagination(form, schema, page, limit):
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        raise HTTPException(status_code=400, detail="page and limit must be integers!")
    if page < 0 or limit < 0 :
        raise HTTPException(status_code=400, detail="page and limit must be positive integers!")
    elif page and limit :
        return {
            "current_page": page,
            "limit": limit,
            "pages": math.ceil(form.count() / limit),
            "data": [schema.from_orm(result) for result in form.offset((page - 1) * limit).limit(limit).all()]
            }
    else :
        return [schema.from_orm(result) for result in form.all()]


async def send_notification(title, body, token):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    try:
        response = messaging.send(message)
        return {"success": True, "message_id": response}
    except Exception as e:
        raise HTTPException(status_code=200, detail="Tasdiqlandi")


def process_excel_tasks(file_bytes: bytes, db: Session, current_user: UsersResponse):
    try:
        excel_data = pd.read_excel(BytesIO(file_bytes), engine=None)
        excel_data.columns = [str(col).strip().lower() for col in excel_data.columns]
    except Exception as e:
        raise Exception(f"Excel faylni o'qib bo'lmadi: {e}")

    for index, row in excel_data.iterrows():
        title = str(row.get("title", "")).strip()
        text = str(row.get("text", "")).strip()

        if not title or not text:
            continue

        existing_task = db.query(Tasks).filter_by(user_id=current_user.id, title=title).first()
        if existing_task:
            continue

        task = Tasks(
            title=title,
            text=text,
            user_id=current_user.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(task)
    db.commit()