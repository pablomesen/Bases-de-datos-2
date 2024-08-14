import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import DATABASE_URL
from ..models.user import UserRole, UserCreate
from ..models.post import PostType, PostCreate
import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/keycloak")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))

class PostDB(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    post_type = Column(Enum(PostType))
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Database:
    def __init__(self):
        self.engine = engine
        Base.metadata.create_all(bind=self.engine)

    def create_user(self, user: UserCreate):
        db_user = UserDB(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_token(self, token: str):
        # Implementar lógica para obtener usuario por token
        pass

    def is_admin(self, token: str):
        user = self.get_user_by_token(token)
        return user.role == UserRole.ADMIN

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
