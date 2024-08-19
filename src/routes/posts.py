# Este código se debe encargar de manejar las rutas relacionadas con los posts. Debe permitir crear, leer, actualizar y eliminar posts, usando la base de datos definida en utils.py y debe validar que el usuario tenga los permisos necesarios para realizar estas acciones.

from fastapi import APIRouter, Depends, HTTPException
from ..models.post import PostCreate, Post
from ..auth.jwt_handler import get_current_user
from ..utils import Database

router = APIRouter()
db = Database()

"""Ejemplo de lo que hace en práctica: """
# localhost:8000/posts/get_posts (esto se ingresa por la terminal y se obtiene un json con los posts o un mensaje de error), así para el resto de los métodos
# En cada método se llama a la base de datos para obtener, crear, actualizar o eliminar los posts.
# Se puede hacer ya sea dentro de la función o llamar un store procedure que haga la operación en la base de datos.

# Todo este código modifiquenlo como quieran, igual el de los models, el de routes/users.py y el de utils/db.py

@router.post("/", response_model=Post)
async def create_post(post: PostCreate, current_user: str = Depends(get_current_user)):
    return db.create_post(post, current_user)

@router.get("/", response_model=list[Post])
async def read_posts(skip: int = 0, limit: int = 100):
    return db.get_posts(skip, limit)

@router.get("/get_posts", response_model=Post)
async def read_post(post_id: int):
    post = db.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return post

@router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post: PostCreate, current_user: str = Depends(get_current_user)):
    user = db.get_user_by_token(current_user)
    if user.role == "reader":
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar posts")
    updated_post = db.update_post(post_id, post, user.id)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    return updated_post

@router.delete("/{post_id}")
async def delete_post(post_id: int, current_user: str = Depends(get_current_user)):
    user = db.get_user_by_token(current_user)
    if user.role not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar posts")
    if db.delete_post(post_id, user.id):
        return {"message": "Post eliminado"}
    raise HTTPException(status_code=404, detail="Post no encontrado")
