from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey

class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(nullable=False)
    descripcion: Mapped[str] = mapped_column(nullable=False)
    estado: Mapped[str] = mapped_column(nullable=False)
    prioridad: Mapped[str] = mapped_column(nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    
