# Endpoint en el que se pueden realizar las operaciones CRUD para los posts.
from fastapi import APIRouter, Depends, HTTPException
from ..models.post import post, post_type
from ..auth.jwt_handler import get_current_userToken
from ..db import DBInstance

router = APIRouter()
