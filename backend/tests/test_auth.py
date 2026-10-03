from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    response = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    assert response.status_code == 200



def test_login_incorrecto():
    response = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P123435"
        }
    )

    assert response.status_code == 401