from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    email = Column(String(255), unique=True)
    token = Column(String(255))
    name = Column(String(255))
    phone = Column(String(255))
    firebase_token = Column(String(255), nullable=True)

    tasks = relationship("Tasks", back_populates="user")


class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(255), unique=True)
    text = Column(String(255))
    status = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship("Users", back_populates="tasks")


class Bots(Base):
    __tablename__ = "bots"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    token = Column(String(255))
    channel_id = Column(String(255))





