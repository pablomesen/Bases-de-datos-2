# Endpoint en el que se pueden realizar las operaciones CRUD para los usuarios.
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..models.user import User, UserDB, KCUserCreate, UserRegisterResponse, LoginRequest, UserToken, PostBase
from ..models.post import Post, post_type
from ..db import DBInstance
from ..auth.keycloak_config import get_keycloak_admin
from ..auth.jwt_handler import generate_user_token, get_current_userId, TokenInfo

router = APIRouter()

# Endpoint para registrar un usuario en la base de datos y en Keycloak
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

        # Crear usuario en la base de datos
        db_user = UserDB(
            name=user.name,
            username=user.username,
            email=user.email,
            password=user.password,
            is_active=True)
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
                new_keycloak_user_id = keycloak_admin.get_user_id(user.username)
                keycloak_admin.delete_user(new_keycloak_user_id)
        except:
            pass  # Si falla la eliminación en Keycloak, simplemente continúa
        print(f"Error detallado: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error en el registro: {str(e)}")

# Enpoint para realizar login de un usuario
@router.post("/login")
async def login_user(login_request: LoginRequest, db: Session = Depends(DBInstance.get_db)):
    try:
        # Verificar si el usuario existe en Keycloak
        keycloak_admin = get_keycloak_admin()
        users = keycloak_admin.get_users()
        user = next((u for u in users if u['username'] == login_request.username), None)
        if not user:
            raise HTTPException(status_code=400, detail="Usuario no encontrado en Keycloak")
        
        # Verificar si el usuario existe en la base de datos
        db_user = db.query(UserDB).filter(UserDB.username == login_request.username).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="Usuario no encontrado en la base de datos")
        
        # Generar un token de acceso
        access_token = generate_user_token(login_request.username, login_request.password)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error en el login: {str(e)}")

# Endpoint para hacer logout de un usuario en Keycloak
@router.post("/logout")
async def logout_user(token: str = Depends(get_current_userId)):
    try:
        keycloak_admin = get_keycloak_admin()
        keycloak_admin.user_logout(token)
        return {"message": "Logout realizado con éxito"}
    except Exception as e:
        print(f"Error detallado: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error en el logout: {str(e)}")

# Endpoint para eliminar un usuario de la base de datos y de Keycloak
@router.delete("/delete/{username}", response_model=dict, response_class=JSONResponse)
async def delete_user(username: str, token: TokenInfo = Depends(TokenInfo.get_current_userId), db: Session = Depends(DBInstance.get_db)):
    print(token.roles)

    # Verifica que el usuario tenga el rol de 'admin'
    if "admin" not in token.roles:
        raise HTTPException(status_code=403, detail="No tiene permisos para realizar esta acción")
    
    print("Verificación de roles exitosa")
    
    # Buscar al usuario en la base de datos
    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")
    
    # Realiza una eliminación lógica en la base de datos
    print(f"Usuario encontrado: {db_user}")
    db_user.is_active = False
    db.commit()

    print("Eliminación lógica en la base de datos realizada")

    # Eliminar al usuario en Keycloak
    keycloak_admin = get_keycloak_admin()
    try:
        keycloak_user_id = keycloak_admin.get_user_id(username)
        keycloak_admin.delete_user(keycloak_user_id)
        print("Usuario eliminado en Keycloak")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error eliminando al usuario en Keycloak: {str(e)}")
    
    return {"message": f"Usuario {username} eliminado con éxito"}

@router.put("/update/{username}", response_model=dict, response_class=JSONResponse)
async def update_user(username: str, user: User, token: TokenInfo = Depends(TokenInfo.get_current_userId), db: Session = Depends(DBInstance.get_db)):

    # Verificar si el usuario existe en la base de datos, de ser así, lo obtiene
    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")
    if db_user.is_active == False:
        raise HTTPException(status_code=400, detail="Usuario desactivado")
    
    # Verifica que el usuario tenga el rol de 'admin'
    if "admin" not in token.roles:
        if "editor" not in token.roles:
            raise HTTPException(status_code=403, detail="No tiene permisos para realizar esta acción")
        else:
            # Verifica que el usuario sea el dueño del perfil
            if token.username != username:
                raise HTTPException(status_code=403, detail="No tiene permisos para realizar esta acción")
            
            # Actualizar información en la base de datos
            db_user.username = user.username
            db_user.email = user.email
            db_user.name = user.name
            db_user.password = user.password
            db.commit()
            db.refresh(db_user)
            
            # Actualizar información en Keycloak
            keycloak_admin = get_keycloak_admin()
            try:
                keycloak_user_id  = keycloak_admin.get_user_id(username)
                keycloak_admin.update_user(keycloak_user_id, {
                    "username": user.username,
                    "email": user.email,
                    "firstName": user.name.split()[0] if user.name else "",
                    "lastName": " ".join(user.name.split()[1:]) if user.name and len(user.name.split()) > 1 else "",
                    "credentials": [{
                        "type": "password",
                        "value": user.password,
                        "temporary": False
                    }]
                })
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error actualizando al usuario en Keycloak: {str(e)}")

            return {"message": "Usuario actualizado con éxito"}

    # Es administrador, puede actualizar cualquier perfil
    # Actualizar información en la base de datos
    db_user.username = user.username
    db_user.email = user.email
    db_user.name = user.name
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)

    # Actualizar información en Keycloak
    keycloak_admin = get_keycloak_admin()
    try:
        keycloak_user_id  = keycloak_admin.get_user_id(username)
        print(keycloak_user_id)
        keycloak_admin.update_user(keycloak_user_id, {
            "username": user.username,
            "email": user.email,
            "firstName": user.name.split()[0] if user.name else "",
            "lastName": " ".join(user.name.split()[1:]) if user.name and len(user.name.split()) > 1 else "",
            "credentials": [{
                "type": "password",
                "value": user.password,
                "temporary": False
            }]
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error actualizando al usuario en Keycloak: {str(e)}")


    return {"message": "Usuario actualizado con éxito"}            

@router.post("/posts/")
async def create_post(username: str, postBase: PostBase, token: TokenInfo = Depends(TokenInfo.get_current_userId), db: Session = Depends(DBInstance.get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if 'reader' in token.roles:
        raise HTTPException(status_code=403, detail="No tiene permisos para realizar esta acción")

    try:
        db_post = Post(
            title=postBase.title, 
            content=postBase.content, 
            post_type_id=postBase.post_type_id, 
            user_id=db_user.id
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el post: {str(e)}")
    