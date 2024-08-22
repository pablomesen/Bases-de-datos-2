# Endpoint en el que se pueden realizar las operaciones CRUD para los usuarios.
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from ..models.user import User, UserDB, KCUserCreate, UserRegisterResponse, LoginRequest, UserToken
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

'''
    BORRADO DE USUARIOS DE LA BASE DE DATOS POR USERNAME
    // Solo son ejecutables por un usuario administrador

        VALIDACIONES: 
            - Se debe de validar que el usuario que ejecuta la petición sea administrador
            - Se debe de validar que no se trate de borrar a el mismo
        
        AMBAS VALIDACIONES DEBEN DE SER REALIZADAS CON LA INFOMRACIÓN DE KEYCLOAK
        
@app.delete("/users/{username}")
async def delete_user_by_username(username: str, db: db_dependency):
    db_user = db.query(models.users).filter(models.users.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_active == False:
        raise HTTPException(status_code=400, detail="User is already deactivated")
    db_user.is_active = False  # Setear isActive a False en lugar de borrar al usuario
    db.commit()
    return {"message": "User deactivated successfully"}


    ACTUALIZACIÓN DE INFORMACIÓN DE USUARIOS POR USERNAME
    // Solo ejecutable para usuario 'Administrator' o usuarios "Editor" dueños del perfil

        VALIDACIONES: 
            - Se debe de validar que el usuario que ejecuta la petición sea administrador o editor
            - En caso de que el usuario sea editor, se debe de validar que sea el dueño del perfil que se desea actualizar
        
        AMBAS VALIDACIONES DEBEN DE SER REALIZADAS CON LA INFOMRACIÓN DE KEYCLOAK

@app.put("/users/{username}")
async def update_user(username: str, user: userBase, db: db_dependency):
    db_user = db.query(models.users).filter(models.users.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_active == False:
        raise HTTPException(status_code=400, detail="User is deactivated")
    db_user.username = user.username
    db_user.email = user.email
    db_user.name = user.name
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/posts/")
async def create_post(username: str, post: postBase, db: db_dependency):
    db_user = db.query(models.users).filter(models.users.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        db_user.id
        db_post = models.posts(title=post.title, content=post.content, post_type_id=post.post_type_id, user_id=db_user.id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
'''