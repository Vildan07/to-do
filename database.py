from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/todo"

Base = declarative_base()

engine = create_engine(DATABASE_URL)

SessionLocal =sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()