import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.usuarios import router
from app.routes.tareas import tarea


load_dotenv()
clave_jwt= os.getenv("JWT_SECRET_KEY")

if not clave_jwt:
    raise RuntimeError(
        "No se encontro JWT_SECRET_KEY en el archivo .env"
    )

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)
app.include_router(router)
app.include_router(tarea)


@app.get("/")
def main():
    return {
        "message": "Bienvenido usuario"
    }