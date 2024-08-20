# Se define la configuración de la DB y de Keycloak que se usará en la aplicación.
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://tc01:basesdedatos2024@postgresdb.cfse8m80m5up.us-east-2.rds.amazonaws.com:5432/app")
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "myrealm")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "myclient")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "mysecret")
KEYCLOAK_ADMIN_USER = os.getenv("KEYCLOAK_ADMIN_USER", "admin")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD", "admin")
