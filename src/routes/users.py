# Este código se debe encargar de definir los endpoints para la creación, lectura, actualización y eliminación de usuarios. Debe validar que el usuario tenga los permisos necesarios para realizar estas acciones.

from fastapi import APIRouter, Depends, HTTPException
from ..models.user import UserCreate, User
from ..auth.jwt_handler import get_current_user
from ..utils import Database

router = APIRouter()
db = Database()
