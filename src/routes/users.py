from fastapi import APIRouter, Depends, HTTPException
from ..models.user import UserCreate, User
from ..auth.jwt_handler import get_current_user
from ..utils.db import Database

router = APIRouter()
db = Database()

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    return db.create_user(user)

@router.get("/me", response_model=User)
async def read_user_me(current_user: str = Depends(get_current_user)):
    return db.get_user_by_token(current_user)

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate, current_user: str = Depends(get_current_user)):
    if not db.is_admin(current_user):
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")
    return db.update_user(user_id, user)

@router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: str = Depends(get_current_user)):
    if not db.is_admin(current_user):
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta acción")
    db.delete_user(user_id)
    return {"message": "Usuario eliminado"}
