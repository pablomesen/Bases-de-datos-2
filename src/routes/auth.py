from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.keycloak_auth import get_token, get_current_user, Token, TokenData

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    token = get_token(form_data.username, form_data.password)
    return {"access_token": token["access_token"], "token_type": "bearer"}

@router.get("/users/me", response_model=TokenData)
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    return current_user
