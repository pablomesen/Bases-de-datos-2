# Este código recibe un token, lo decodifica y devuelve el token. Si no, devuelve un error 401.
import requests
from jose import JWTError, jwt
from typing import List
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .keycloak_config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET, JWT_SECRET_KEY, JWT_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def get_current_userId(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], audience=KEYCLOAK_CLIENT_ID)
        user_id: str = payload.get("sub")
    except JWTError as e:
        raise HTTPException(status_code=400, detail=f"Credenciales inválidas: {str(e)}")
    return user_id

class TokenInfo(BaseModel):
    username: str
    email: str
    roles: List[str]

    @classmethod
    def from_token(cls, token: str) -> 'TokenInfo':
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            username: str = payload.get("preferred_username")
            email: str = payload.get("email")
            roles: List[str] = payload.get("resource_access", {}).get("account", {}).get("roles", [])
            return cls(username=username, email=email, roles=roles)
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def generate_user_token(username, password):
    token_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
    token_data = {
        "grant_type": "password",
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "username": username,
        "password": password
    }
    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Acceso denegado: Credenciales inválidas")
    token = token_response.json()
    return token["access_token"]
