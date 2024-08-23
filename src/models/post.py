# Se representa la estructura de la tabla post y post_type en la base de datos
# Se representa la estructura de la tabla post y post_type en la base de datos
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from ..db import DBInstance

class Post(DBInstance.Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_type_id = Column(Integer, ForeignKey("post_types.id"), nullable=False)

class post_type(DBInstance.Base):
    __tablename__ = "post_types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    post_id = Column(Integer, ForeignKey("posts.id"))
