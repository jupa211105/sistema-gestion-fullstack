from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class CreateTask(BaseModel):
    titulo: str
    descripcion: str
    estado: str
    prioridad: str

class UpdateTask(BaseModel):
    titulo: str
    descripcion: str
    estado: str
    prioridad: str

class ResponseTask(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    prioridad: str
    usuario_id: int
    fecha_creacion: datetime

class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completada = "completada"


class PrioridadTarea(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"