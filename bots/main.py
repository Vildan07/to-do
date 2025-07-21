import httpx

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Bots


async def send_telegram_message(message: str, db: Session):
    data = db.query(Bots).first()
    if not data:
        raise HTTPException(status_code=404, detail="Ma'lumot mavjud emas!")
    url = f"https://api.telegram.org/bot{data.token}/sendMessage"
    payload = {
        "chat_id": data.channel_id,
        "text": message
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        return response.json()
