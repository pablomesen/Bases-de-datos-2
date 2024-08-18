from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .jwt_handler import get_current_user
from jose import JWTError
from .keycloak_config import keycloak_openid
from ..utils.db import Database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    try:
        # Verificar el token con Keycloak
        token_info = keycloak_openid.introspect(token)
        if not token_info.get('active'):
            raise HTTPException(status_code=401, detail="Token inactivo o inválido")
        
        # Obtener el nombre de usuario del token
        username = token_info.get('preferred_username')
        if not username:
            raise HTTPException(status_code=401, detail="No se pudo obtener el nombre de usuario del token")
        
        # Buscar el usuario en la base de datos
        db = Database()
        user = db.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="Usuario no encontrado en la base de datos")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error de autenticación: {str(e)}")

def get_token(username: str, password: str):
    try:
        token = keycloak_openid.token(username, password)
        return token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al obtener el token: {str(e)}")
