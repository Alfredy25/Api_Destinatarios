from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.security.passwords import hash_password
from app.db.database import Base
from app.entities.user import User
from app.dependencies.di import get_db
import time

db_path = os.path.join(os.path.dirname(__file__), 'test.db')
db_uri = f"sqlite:///{db_path}"
SQLALCHEMY_DATABASE_URI = db_uri
engine_test = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
Base.metadata.create_all(engine_test)


def insertar_usuario_prueba():
    password_hash = hash_password("prueba123")
    with TestingSessionLocal() as session:
        usuario = User(
            username="alfredo",
            email="pruebas@gmail.com",
            password_hash=password_hash,
            is_active=True
        )
        session.add(usuario)
        session.commit()

insertar_usuario_prueba()


def override_get_db():
    print("USANDO BASE DE DATOS DE PRUEBA")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

cliente = TestClient(app)

def test_crear_usuario():
    usuario = {
        "username": "juanito",
        "email": "juanito_2@gmail.com",
        "password": "juanito123"
    }
    response = cliente.post("/users/", json=usuario)
    assert response.status_code == 401


    usuario_auth = {
        "email": "pruebas@gmail.com",
        "password": "prueba123"
    }

    response_token = cliente.post("/auth/login", json=usuario_auth)
    assert response_token.status_code == 200
    if response_token.status_code == 200:
        json_data = response_token.json()
        assert json_data.get('token_type') == 'bearer'
        token = json_data.get('access_token')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = cliente.post("/users/", json=usuario, headers=headers)
        assert response.status_code == 201
        assert response.json().get('id') is not None
        print(response.json())

def test_obtener_users():
    usuario_auth = {
        "email": "pruebas@gmail.com",
        "password": "prueba123"
    }

    response_token = cliente.post("/auth/login", json=usuario_auth)
    assert response_token.status_code == 200
    if response_token.status_code == 200:
        json_data = response_token.json()
        assert json_data.get('token_type') == 'bearer'
        token = json_data.get('access_token')
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = cliente.get("/users/", headers=headers)
        assert len(response.json()) > 0
        print(response.json())

# def test_delete_database():
#     time.sleep(7)
#     db_path_act = os.path.join(os.path.dirname(__file__), 'test.db')
#     os.remove(db_path_act)


