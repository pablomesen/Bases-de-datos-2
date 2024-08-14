from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class PostType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"

class PostBase(BaseModel):
    title: str
    content: str
    post_type: PostType

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
