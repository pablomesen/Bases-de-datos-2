from fastapi import APIRouter, Depends, HTTPException
from ..models.post import PostCreate, Post
from ..auth.keycloak import get_current_user
from ..utils.db import Database

router = APIRouter()
db = Database()

@router.post("/", response_model=Post)
async def create_post(post: PostCreate, current_user: str = Depends(get_current_user)):
    return db.create_post(post, current_user)

@router.get("/", response_model=list[Post])
async def read_posts(skip: int = 0, limit: int = 100):
    return db.get_posts(skip, limit)

@router.get("/{post_id}", response_model=Post)
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
