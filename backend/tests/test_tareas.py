from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_crear_tarea():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.post(
        "tareas",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "titulo": "Tarea de prueba",
            "descripcion": "Probando pytest",
            "estado": "pendiente",
            "prioridad": "alta"
        }
    )

    assert response.status_code == 201

def test_listar_tareas():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.get(
        "tareas",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

def test_listar_tareas_id():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.get(
        "tareas/5",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200



def test_actualizar_tarea():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.put(
        "tareas/14",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "titulo": "Tarea de prueba terminada",
            "descripcion": "Probando pytest metodo put",
            "estado": "pendiente",
            "prioridad": "baja"
        }
    )

    assert response.status_code == 200

def test_eliminar_tarea():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.delete(
        "tareas/13",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200



def test_sin_token():
    token = None

    response = client.post(
        "tareas",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "titulo": "Tarea de prueba",
            "descripcion": "Probando pytest",
            "estado": "pendiente",
            "prioridad": "alta"
        }
    )

    assert response.status_code == 401


def test_ID_inexistente():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.put(
        "tareas/90",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "titulo": "Tarea de prueba terminada",
            "descripcion": "Probando pytest metodo put",
            "estado": "pendiente",
            "prioridad": "baja"
        }
    )

    assert response.status_code == 404



def test_listar_tareas_estado_invalido():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.get(
        "tareas?estado=invalido",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 422


def test_listar_tareas_prioridad_invalido():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.get(
        "tareas?prioridad=invalida",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 422



def test_listar_tareas_filtros():
    login = client.post(
        "usuarios/login",
        json={
            "correo": "gil@gmail.com",
            "password": "P12345"
        }
    )

    token = login.json()["token"]

    response = client.get(
        "tareas/dos",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 422
    