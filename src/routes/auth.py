from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.keycloak import get_token, get_current_user

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = get_token(form_data.username, form_data.password)
        return {"access_token": token["access_token"], "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

@router.get("/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
