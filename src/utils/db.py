# Este código se debe encargar de definir la clase Database, que se encarga de manejar la conexión con la base de datos y de definir los métodos necesarios para interactuar con ella. Además, se define la clase UserDB, que representa la tabla de usuarios en la base de datos. También se definen los métodos get_user_by_username y create_user, que permiten buscar un usuario por su nombre de usuario y crear un nuevo usuario, respectivamente.
# Posteriormente, se deben definir las clases para las tablas restantes en la base de datos, así como los métodos necesarios para interactuar con ellas. También se deben definir los métodos necesarios para manejar las rutas relacionadas con los posts y los usuarios, validando que el usuario tenga los permisos necesarios para realizar las acciones correspondientes.

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import DATABASE_URL
from ..models.user import UserCreate

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255))
    Username = Column(String(255), unique=True, index=True)
    Password = Column(String(255))
    IsActive = Column(Integer)
    UserLevel_id = Column(Integer)
    Email = Column(String(255), unique=True, index=True)

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = SessionLocal()

    def get_user_by_username(self, username: str):
        return self.db.query(UserDB).filter(UserDB.Username == username).first()

    def create_user(self, user: UserCreate):
        db_user = UserDB(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
