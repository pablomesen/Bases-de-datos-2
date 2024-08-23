# Se define la configuración de la DB y de Keycloak que se usará en la aplicación.
import os

DATABASE_URL = os.getenv("DATABASE_URL", "myDBurl")
KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "mykeycloakurl")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "myrealm")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "myclient")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "mysecret")
KEYCLOAK_ADMIN_USER = os.getenv("KEYCLOAK_ADMIN_USER", "admin")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD", "admin")
KC_PUBLIC_KEY = os.getenv("KC_PUBLIC_KEY", "mysecretKEY")
