from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import requests
from ..config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token")

def get_keycloak_public_key():
    url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['public_key']

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
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
    except JWTError:
        raise credentials_exception
    return username

def get_token(username: str, password: str):
    data = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    response = requests.post(
        f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
        data=data,
    )
    response.raise_for_status()
    return response.json()

