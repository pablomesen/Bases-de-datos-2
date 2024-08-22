from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from ..db import DBInstance

# Modelos para la tabla de users
class UserDB(DBInstance.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    is_active = Column(Boolean, default=True)

class User(BaseModel):
    id: int
    name: str
    username: str
    email: str
    password: str
    is_active: bool
    class Config:
        from_attributes = True

# Modelos para la tabla de posts

class postBase(BaseModel):
    title: str
    content: str
    post_type_id: int

# Modelos para la creación de usuarios
class KCUserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str

class UserRegisterResponse(BaseModel):
    message: str
    user: User

# Modelo para el inicio de sesión
class LoginRequest(BaseModel):
    username: str
    password: str

class UserToken(BaseModel):
    access_token: str
    token_type: str

class UserRole(BaseModel):
    role: str