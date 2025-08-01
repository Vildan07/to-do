import math
from fastapi import HTTPException
from firebase_admin import messaging

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