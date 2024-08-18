# Este código define un modelo de datos User que es usado para representar un usuario en la base de datos, y un modelo UserCreate que es usado para crear un usuario. Un modelo UserBase que es usado para definir los campos comunes entre User y UserCreate. También define un enumerador UserRole que representa los roles de usuario posibles.

from pydantic import ConfigDict, BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    READER = "reader"

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.READER

class User(BaseModel):
    id: int
    Name: str
    Username: str
    Email: EmailStr
    UserLevel_id: int
    IsActive: bool

    class Config:
        from_attributes = True
