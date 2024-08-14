from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .keycloak_config import keycloak_openid

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_user(token: str = Depends(oauth2)):
    try:
        keycloak_openid.decode_token(token)
        return token
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
