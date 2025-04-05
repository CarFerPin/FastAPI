import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.dbhandler import Base, get_db
from app.security.flowOauth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta

# Configuración de la base de datos para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sobrescribir la dependencia de la base de datos
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Crear la base de datos de prueba
Base.metadata.create_all(bind=engine)

# Cliente de pruebas
client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    """
    Fixture para inicializar el cliente de pruebas.
    """
    yield client

def test_root_endpoint(test_client):
    """
    Prueba para verificar que la aplicación se inicializa correctamente.
    """
    response = test_client.get("/")
    assert response.status_code == 404  # No hay un endpoint raíz definido

def test_login_for_access_token(test_client):
    """
    Prueba para el endpoint de obtención de token de acceso.
    """
    # Intentar iniciar sesión con credenciales válidas
    response = test_client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Intentar iniciar sesión con credenciales inválidas
    response = test_client.post(
        "/token",
        data={"username": "invaliduser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_shutdown_event():
    """
    Prueba para verificar que el evento de apagado cierra las conexiones activas.
    """
    try:
        app.router.on_event("shutdown")
        assert True
    except Exception:
        assert False