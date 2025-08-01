import os
from firebase_admin import credentials, initialize_app

def init_firebase():
    FIREBASE_KEY = os.getenv("FIREBASE_KEY")

    if FIREBASE_KEY:
        with open("serviceAccountKey.json", "w") as f:
            f.write(FIREBASE_KEY)

        cred = credentials.Certificate("serviceAccountKey.json")
        try:
            initialize_app(cred)
        except ValueError:
            # Firebase already initialized
            pass