# Este código define un modelo de datos Post que es usado para representar un post en la base de datos, y un modelo PostCreate que es usado para crear un post. Un modelo PostBase que es usado para definir los campos comunes entre Post y PostCreate. También define un enumerador PostType que representa los tipos de post posibles.

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

class Post(BaseModel):
    id: int
    texto: str
    user_id: int
    post_type_id: int
    url: str
    model_config = ConfigDict(from_attributes=True)
