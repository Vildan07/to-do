from firebase_admin import credentials, initialize_app
import os

def init_firebase():
    if os.path.exists("serviceAccountKey.json"):
        cred = credentials.Certificate("serviceAccountKey.json")
        try:
            initialize_app(cred)
        except ValueError:
            # Already initialized
            pass