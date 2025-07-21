from fastapi import APIRouter, HTTPException
from firebase_admin import credentials, messaging, initialize_app


firebase_router = APIRouter(tags=['Firebases'])


cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
