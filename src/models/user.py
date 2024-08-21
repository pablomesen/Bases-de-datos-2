from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from ..db import DBInstance

class UserDB(DBInstance.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    is_active = Column(Boolean, default=False)

class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    password: str
    is_active: bool
    class Config:
        from_attributes = True

class KCUserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str

class UserRegisterResponse(BaseModel):
    message: str
    user: User
