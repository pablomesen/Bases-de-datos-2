# Este código recibe un token, lo decodifica y devuelve el token. Si no, devuelve un error 401.
import requests
from jose import JWTError, jwt
from typing import List
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from ..config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET, KC_PUBLIC_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def get_current_userId(token: str = Depends(oauth2_scheme)):
    try:
      payload = jwt.decode(token, KC_PUBLIC_KEY, algorithms=["RS256"], audience=KEYCLOAK_CLIENT_ID)
      user_id = payload.get("sub")
    except JWTError as e:
        raise HTTPException(status_code=400, detail=f"Credenciales inválidas: {str(e)}")
    return user_id

# Define la clase TokenInfo que representa la información extraída del token
class TokenInfo(BaseModel):
    user_id: str
    username: str
    email: str
    roles: List[str]

    @classmethod
    async def get_current_userId(cls, token: str = Depends(oauth2_scheme)):
        try:
            # Decodifica el token JWT utilizando la clave pública y el cliente de Keycloak
            payload = jwt.decode(token, KC_PUBLIC_KEY, algorithms=["RS256"], audience=KEYCLOAK_CLIENT_ID)
            user_id = payload.get("sub")
            username = payload.get("preferred_username")
            email = payload.get("email")

            # Extrae los roles del token, revisando tanto la sección "account" como "myclient"
            roles_account = payload.get("resource_access", {}).get("account", {}).get("roles", [])
            roles_myclient = payload.get("resource_access", {}).get(KEYCLOAK_CLIENT_ID, {}).get("roles", [])
            roles = roles_account + roles_myclient

            return cls(user_id=user_id, username=username, email=email, roles=roles)
        except JWTError as e:
            raise HTTPException(status_code=400, detail=f"Credenciales inválidas: {str(e)}")

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
