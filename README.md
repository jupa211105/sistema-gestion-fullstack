# Sistema de Gestión Fullstack

Sistema web completo para la gestión de usuarios y tareas, desarrollado con una arquitectura separada entre frontend, backend y base de datos.

El proyecto implementa autenticación mediante JWT, gestión de tareas por usuario, persistencia con PostgreSQL, migraciones con Alembic, pruebas automatizadas y ejecución mediante Docker Compose.

---

##  Tecnologías

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT
- pwdlib / Argon2
- Pytest
- Uvicorn

### Frontend

- React
- Vite
- React Router
- JavaScript
- HTML
- CSS

### Infraestructura

- Docker
- Docker Compose
- Nginx

---

##  Arquitectura

```text


                    ┌─────────────────┐
                    │     React       │
                    │    Frontend     │
                    └────────┬────────┘
                             │
                         HTTP / JSON
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │     Backend     │
                    └────────┬────────┘
                             │
                        SQLAlchemy
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │    Database     │
                    └─────────────────┘
```
---


##  Estructura del proyecto

```text

sistema-gestion-fullstack/
│
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── app/
│   │   ├── dependencies/
│   │   │   └── auth.py
│   │   │
│   │   ├── models/
│   │   │   ├── tareas.py
│   │   │   └── usuario.py
│   │   │
│   │   ├── routes/
│   │   │   ├── tareas.py
│   │   │   └── usuarios.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── tareas.py
│   │   │   └── usuario.py
│   │   │
│   │   ├── services/
│   │   │   ├── seguridad.py
│   │   │   ├── tareas.py
│   │   │   ├── tokens.py
│   │   │   └── usuarios.py
│   │   │
│   │   ├── database.py
│   │   ├── main.py
│   │   └── __init__.py
│   │
│   ├── tests/
│   │   ├── test_auth.py
│   │   └── test_tareas.py
│   │
│   ├── alembic.ini
│   └── requirements.txt
│
├── docker/
│   ├── backend/
│   │   └── Dockerfile
│   │
│   └── frontend/
│       └── Dockerfile
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Editar.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Registrar.jsx
│   │   │   └── Tareas.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---


## Funcionalidades
### Usuarios
El sistema permite:
- Registrar usuarios.
- Iniciar sesión.
- Generar tokens JWT.
- Proteger endpoints mediante autenticación.
- Consultar información del usuario autenticado.
- Cerrar sesión mediante revocación del token.
- Validar tokens expirados.
- Validar tokens inválidos.
- Validar tokens revocados.
- Almacenar contraseñas utilizando hash seguro.
Las contraseñas nunca se almacenan directamente en la base de datos.

## Gestion de tareas
Cada usuario puede gestionar sus propias tareas.
Operaciones disponibles:
- Crear tareas.
- Consultar tareas.
- Consultar una tarea específica.
- Actualizar tareas.
- Eliminar tareas.
- Filtrar tareas por estado.
- Filtrar tareas por prioridad.

### Estados disponibles
    pendiente
    en_progreso
    completada

### Prioridades disponibles
    baja
    media
    alta

    Las tareas están asociadas al usuario que las creó y los endpoints protegidos verifican la propiedad de las tareas.


## Autenticacion
La API utiliza JWT para autenticar las peticiones protegidas.
El flujo general es:
```text


1. Usuario inicia sesión
          │
          ▼
2. FastAPI valida correo y contraseña
          │
          ▼
3. Se genera JWT
          │
          ▼
4. React guarda el token
          │
          ▼
5. React envía:
   Authorization: Bearer <token>
          │
          ▼
6. FastAPI valida el JWT
          │
          ▼
7. Se permite el acceso al recurso
```


El token contiene información como:
```text

- sub → ID del usuario
- jti → identificador único del token
- exp → fecha de expiración
```

Para el cierre de sesión se utiliza el jti del token y se almacena como revocado.

## Bases de datos
El proyecto utiliza PostgreSQL.
La conexión se configura mediante una variable de entorno:
DATABASE_URL=postgresql+psycopg2://usuario:password@db:5432/sistema_gestion

Cuando se ejecuta mediante Docker Compose, el hostname:
db

corresponde al servicio PostgreSQL definido en docker-compose.yml.

## Migraciones
Para ejecutar las migraciones dentro del contenedor:
docker compose exec backend alembic upgrade head

Para crear una nueva migración:
docker compose exec backend alembic revision --autogenerate -m "descripcion_de_la_migracion"

Después:
docker compose exec backend alembic upgrade head

## Docker

Docker
El proyecto utiliza tres servicios principales:
```text

┌─────────────────────────┐
│        frontend         │
│      React + Nginx      │
│        Port 5173        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│        backend          │
│     FastAPI + Uvicorn   │
│        Port 8000        │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│           db            │
│       PostgreSQL 16     │
│        Port 5432        │
└─────────────────────────┘

```


PostgreSQL utiliza un volumen Docker para conservar los datos cuando el contenedor se recrea.

## Variables de entorno

El backend utiliza un archivo .env.
Ejemplo:
DATABASE_URL=postgresql+psycopg2://postgres:TU_PASSWORD@db:5432/sistema_gestion

JWT_SECRET_KEY=TU_SECRET_KEY
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

### Pruebas
El backend utiliza Pytest.
Para ejecutar todas las pruebas localmente:
cd backend
python -m pytest

También pueden ejecutarse dentro del contenedor:
docker compose exec backend python -m pytest

Las pruebas cubren principalmente:
- Registro de usuarios.
- Login.
- Autenticación.
- Tokens JWT.
- Revocación de tokens.
- Creación de tareas.
- Consulta de tareas.
- Actualización de tareas.
- Eliminación de tareas.
- Validación de acceso a tareas.

## Seguridad

El proyecto implementa varias medidas de seguridad:
- Contraseñas almacenadas mediante hash.
- Autenticación mediante JWT.
- Tokens con fecha de expiración.
- Identificador único (jti) para cada token.
- Revocación de tokens.
- Protección de rutas mediante dependencias de FastAPI.
- Variables sensibles mediante .env.
- Separación entre modelos, schemas, servicios y rutas.
- Validación de datos mediante Pydantic.


```text


