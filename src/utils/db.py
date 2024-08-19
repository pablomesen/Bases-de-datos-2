# Este código se debe encargar de definir la clase Database, que se encarga de manejar la conexión con la base de datos y de definir los métodos necesarios para interactuar con ella. Además, se define la clase UserDB, que representa la tabla de usuarios en la base de datos. También se definen los métodos get_user_by_username y create_user, que permiten buscar un usuario por su nombre de usuario y crear un nuevo usuario, respectivamente.
# Posteriormente, se deben definir las clases para las tablas restantes en la base de datos, así como los métodos necesarios para interactuar con ellas. También se deben definir los métodos necesarios para manejar las rutas relacionadas con los posts y los usuarios, validando que el usuario tenga los permisos necesarios para realizar las acciones correspondientes.

import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import DATABASE_URL
from ..models.user import UserRole, UserCreate
from ..models.post import PostType, PostCreate

Base = declarative_base()

class UserDB(Base): # Modelo de la tabla Users -> Puede hacerse acá en vez de /models
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255))
    Username = Column(String(255), unique=True, index=True)
    Password = Column(String(255))
    IsActive = Column(Integer)
    UserLevel_id = Column(Integer)
    Email = Column(String(255), unique=True, index=True)

class PostDB(Base): # Modelo de la tabla Posts -> Puede hacerse acá en vez de /models
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, index=True)
    Title = Column(String(255))
    Content = Column(String(255))
    Author_id = Column(Integer)

class PostCreate(Base):
    pass

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
    
    def is_admin(self, token: str):
        user = self.get_user_by_token(token)
        return user and user.role == UserRole.ADMIN

    def update_user(self, user_id: int, user: UserCreate):
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        self.db.delete(db_user)
        self.db.commit()

    def create_post(self, post: PostCreate, author_id: int):
        db_post = PostDB(**post.dict(), author_id=author_id)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post

    def get_posts(self, skip: int = 0, limit: int = 100):
        return self.db.query(PostDB).offset(skip).limit(limit).all()

    def get_post(self, post_id: int):
        return self.db.query(PostDB).filter(PostDB.id == post_id).first()

    def update_post(self, post_id: int, post: PostCreate, author_id: int):
        db_post = self.db.query(PostDB).filter(PostDB.id == post_id, PostDB.author_id == author_id).first()
        if db_post:
            for key, value in post.dict().items():
                setattr(db_post, key, value)
            db_post.updated_at = datetime.datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_post)
        return db_post

    def delete_post(self, post_id: int, author_id: int):
        db_post = self.db.query(PostDB).filter(PostDB.id == post_id, PostDB.author_id == author_id).first()
        if db_post:
            self.db.delete(db_post)
            self.db.commit()
            return True
        return False
    