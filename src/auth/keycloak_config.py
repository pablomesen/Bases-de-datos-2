# Contiene la configuración de keycloak para la autenticación de usuarios y la creación de usuarios en la base de datos.
from keycloak import KeycloakAdmin
from ..config import KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET

def get_keycloak_admin():
    return KeycloakAdmin(
        server_url=KEYCLOAK_URL,
        realm_name=KEYCLOAK_REALM,
        client_id=KEYCLOAK_CLIENT_ID,
        client_secret_key=KEYCLOAK_CLIENT_SECRET,
        verify=True
    )
