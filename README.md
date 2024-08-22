----------------------------------------------------------------------------------------------------------------------------
IC4302 - Bases de Datos II
TC01 - Despliegue de Aplicaciones con Docker y PostgreSQL
Autores:
  - Daniel Zeas Brown
  - Esteban Josué Solano Araya
  - Pablo Mauricio Mesén Alvarado 
----------------------------------------------------------------------------------------------------------------------------
Explicación del código:

  1. Estructura general: 
    - La aplicación está construida con FastAPI, un framework moderno para crear APIs con Python.
    - Utiliza SQLAlchemy como ORM para interactuar con la base de datos PostgreSQL.
    - Keycloak se utiliza para la autenticación y autorización.
  2. Autenticación con Keycloak:
    - El archivo src/auth/keycloak.py maneja la interacción con Keycloak.
    - get_keycloak_public_key() obtiene la clave pública de Keycloak para verificar tokens.
    - get_current_userId() valida el token JWT y extrae el id de usuario.
    - get_token() se utiliza para obtener un token de acceso de Keycloak.
  3. Interacción con la base de datos:
    - src/utils/db.py contiene la clase Database que maneja todas las operaciones de la base de datos.
    - Utiliza SQLAlchemy y Pydantic para definir modelos (UserDB y PostDB) que se mapean a tablas en la base de datos.
    - Proporciona métodos CRUD para usuarios y posts.
  4. Rutas API:
    - src/routes/ contiene los archivos que definen los endpoints de la API.
    - Utilizan dependencias de FastAPI para manejar la autenticación y autorización.

----------------------------------------------------------------------------------------------------------------------------

Tutorial paso a paso de uso de la RestAPI para autenticación con Keycloak y Interacción con BD (en terminal con admin privileges):
  1. Instalación de dependencias:
    - poetry install --no-root
  2. Iniciar la app:
    docker-compose up --build
  3. Configurar Keycloak: (Esto ya debería de estar realizado automáticamente) 
    a. Acceder a http://localhost:8080
    b. Iniciar sesión con usuario "admin" y contraseña "admin"
    c. Crear un nuevo realm llamado "myrealm"
    d. En el realm "myrealm", crear un nuevo cliente:
      - Client ID: myclient
      - Client Protocol: openid-connect
      - Access Type: confidential
      - Valid Redirect URIs: http://localhost:8000/*
    e. Después de crear el cliente, ir a la pestaña "Credentials" y copiar el "Secret" en el .env
    f. Crear un nuevo usuario en el realm:
      - Username: testuser
      - Email: testuser@example.com
      - Crear una contraseña para el user
  4. Interactuar con la base de datos con pgAdmin:
    a. Acceder a pgAdmin en http://localhost:5050
    b. Iniciar sesión con el email "admin@example.com" y contraseña "admin"
    c. Agregar un nuevo servidor: (Una vez se hace la conexión ya se conecta automáticamente al ingresar debido al volume)
      - La información de conectividad se encuentra en el
        archivo de texto "ConnectionInfo.txt"
      - La base de datos esta ubicada en la nube utilizando los servicios de AWS, por lo que la persistencia de datos es practicamente garantizada
    e. Desde pgAdmin se puede interactuar de manera libre con la base de datos.
  5. Uso de la API:
    a. Registrarse a la app:

----------------------------------------------------------------------------------------------------------------------------
COMANDOS CURL
- Registro de user: 
  curl -X POST "http://localhost:8000/users/register" -H "Content-Type: application/json" -d '{"name": "","username": "","email": "","password": ""}'

- Login:
  curl -X POST "http://localhost:8000/users/login" -H "Content-Type: application/json" -d '{"username": "admin","password": "123"}'

- Logout:
  curl -X POST "http://localhost:8000/users/logout" -H "Authorization: Bearer <token_obtenido>"

- Delete:
  curl -X DELETE "http://localhost:8000/users/delete/curl" -H "Authorization: Bearer <token_obtenido>" -H "Content-Type: application/json"