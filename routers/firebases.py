import os
from fastapi import APIRouter, HTTPException
from firebase_admin import credentials, messaging, initialize_app

firebase_router = APIRouter(tags=['Firebase'])

FIREBASE_KEY = os.getenv("FIREBASE_KEY")

if FIREBASE_KEY:
    with open("serviceAccountKey.json", "w") as f:
        f.write(FIREBASE_KEY)

    cred = credentials.Certificate("serviceAccountKey.json")
    initialize_app(cred)
else:
    cred = None  # Можно обработать иначе
