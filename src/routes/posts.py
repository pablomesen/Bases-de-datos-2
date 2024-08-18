# Este código se debe encargar de manejar las rutas relacionadas con los posts. Debe permitir crear, leer, actualizar y eliminar posts, usando la base de datos definida en utils.py y debe validar que el usuario tenga los permisos necesarios para realizar estas acciones.

from fastapi import APIRouter, Depends, HTTPException
from ..models.post import PostCreate, Post
from ..auth.jwt_handler import get_current_user
from ..utils import Database

router = APIRouter()
db = Database()
