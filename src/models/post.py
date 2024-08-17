from pydantic import ConfigDict, BaseModel
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
    model_config = ConfigDict(from_attributes=True)
