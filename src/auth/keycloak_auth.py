# Este archivo hace lo mismo que keycloak.py pero con la diferencia de que se usa el módulo requests para hacer las peticiones HTTP.
# Estoy probando opciones porque la authenticación con keycloak sigue sin funcionar.

import requests
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import Optional
from ..config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def get_keycloak_public_key():
    url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['public_key']
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch Keycloak public key: {str(e)}")

def get_token(username: str, password: str):
    data = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        public_key = get_keycloak_public_key()
        payload = jwt.decode(
            token,
            f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----",
            algorithms=["RS256"],
            audience=KEYCLOAK_CLIENT_ID,
        )
        username: str = payload.get("preferred_username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data
