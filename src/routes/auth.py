# Este código se debe encargar de manejar las rutas relacionadas con la autenticación de usuarios. Debe tener una ruta para iniciar sesión, una para cerrar sesión y una para obtener información del usuario actual. También debe tener un decorador para verificar si el usuario está autenticado.
# No sé si debe tener conexión a la base de datos para verificar que las credenciales del usuario existan en la base de datos.

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..auth.keycloak import get_current_active_user, get_token, get_current_user
from ..models.user import User

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = get_token(form_data.username, form_data.password)
    return {"access_token": token["access_token"], "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
