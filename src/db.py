from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Annotated
from .config import DATABASE_URL

# Definir los esquemas Pydantic para la validación de datos
class userBase(BaseModel):
    name: str
    username: str
    email: str
    password: str
    is_active: bool

class postBase(BaseModel):
    title: str
    content: str

class postTypeBase(BaseModel):
    type: str

# Definir la clase Database para la conexión a la base de datos.
class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    # Función que crea la sesión de la base de datos
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

DBInstance = Database()
