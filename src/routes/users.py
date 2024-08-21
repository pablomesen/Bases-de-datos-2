# Endpoint en el que se pueden realizar las operaciones CRUD para los usuarios.
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models.user import User, UserDB, KCUserCreate, UserRegisterResponse
from ..db import DBInstance
from ..auth.keycloak_config import get_keycloak_admin

router = APIRouter()

@router.post("/register", response_model=UserRegisterResponse)
async def register_user(user: KCUserCreate, db: Session = Depends(DBInstance.get_db)):
    try:
        # Crear usuario en Keycloak
        keycloak_admin = get_keycloak_admin()
        new_keycloak_user = keycloak_admin.create_user({
            "username": user.username,
            "email": user.email,
            "firstName": user.name.split()[0] if user.name else "",
            "lastName": " ".join(user.name.split()[1:]) if user.name and len(user.name.split()) > 1 else "",
            "enabled": True,
            "emailVerified": True,
            "credentials": [{
                "type": "password",
                "value": user.password,
                "temporary": False
            }]
        })

        print(f"Usuario creado en Keycloak: {new_keycloak_user}")
        usuarios = keycloak_admin.get_users()
        print(f"Usuarios en Keycloak: {usuarios}")
        # Obtener el ID del usuario creado en Keycloak
        new_keycloak_user_id = keycloak_admin.get_user_id(user.username)
        print(f"ID del usuario en Keycloak: {new_keycloak_user_id}")

        # Crear usuario en la base de datos
        db_user = UserDB(
            name=user.name,
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return {"message": "Usuario registrado con éxito", "user": User.model_validate(db_user)}
    except Exception as e:
        # Si algo sale mal, revertir cualquier cambio parcial
        db.rollback()
        # Intenta eliminar el usuario de Keycloak si se creó
        try:
            if new_keycloak_user:
                keycloak_admin.delete_user(new_keycloak_user_id)
        except:
            pass  # Si falla la eliminación en Keycloak, simplemente continúa
        print(f"Error detallado: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error en el registro: {str(e)}")

# # Aún no se ha probado esta función
# async def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = DBInstance.db_session):
#     try:
#         # Verificar el token con Keycloak
#         token_info = keycloak_openid.introspect(token)
#         if not token_info.get('active'):
#             raise HTTPException(status_code=401, detail="Token inactivo o inválido")
        
#         # Obtener el nombre de usuario del token
#         username = token_info.get('preferred_username')
#         if not username:
#             raise HTTPException(status_code=401, detail="No se pudo obtener el nombre de usuario del token")
        
#         # Buscar el usuario en la base de datos
#         user = db.get_user_by_username(username)
#         if not user:
#             raise HTTPException(status_code=401, detail="Usuario no encontrado en la base de datos")
        
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=401, detail=f"Error de autenticación: {str(e)}")
