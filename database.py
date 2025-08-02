from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()

engine = create_engine("mysql+pymysql://root:cQdtLwArhTfradHhNcihKoiOwTlifeMY@mysql-eemf.railway.internal:3306/railway")
# engine = create_engine("mysql+pymysql://root:123456@localhost:3306/todo")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()