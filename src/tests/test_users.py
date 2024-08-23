import pytest
from fastapi import HTTPException
from jose import jwt, JWTError
from ..auth.jwt_handler import get_current_userId

# Claves y datos de prueba
public_key = "your-public-key"
KEYCLOAK_CLIENT_ID = "your-client-id"

@pytest.fixture
def valid_token():
    payload = {
        "sub": "123456",
        "preferred_username": "testuser",
        "email": "testuser@example.com",
        "resource_access": {
            "account": {
                "roles": ["user"]
            },
            "your-client-id": {
                "roles": ["admin"]
            }
        }
    }
    return jwt.encode(payload, public_key, algorithm="RS256")

@pytest.fixture
def invalid_token():
    return "invalidtoken"

def test_get_current_userId_valid_token(valid_token):
    result = get_current_userId(valid_token)
    assert result == "123456"

def test_get_current_userId_invalid_token(invalid_token):
    with pytest.raises(HTTPException, match="Credenciales inválidas"):
        get_current_userId(invalid_token)

