from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from app.schemas.tareas import CreateTask, UpdateTask, PrioridadTarea, EstadoTarea
from app.database import get_db
from app.dependencies.auth import verificar_token
from app.services.tareas import crear_tarea, buscar_tareas, buscar_tarea, actualizar_tarea, eliminar_tarea



tarea = APIRouter(prefix="/tareas")

@tarea.post("")
def crear_tarea_endpoint(tarea: CreateTask, datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_id, jti = datos_token
    try:
        valido, resultado = crear_tarea(tarea, usuario_id, db)

        if valido:
            return JSONResponse(
                status_code=201,
                content={
                    "status": "ok",
                    "message": "Tarea creada correctamente",
                    "ID": resultado
                }
            )

        else:
            return JSONResponse(
                status_code=401,
                content={
                    "status": "error",
                    "message": resultado
                }
            )
    

    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Error de integracion en la BD"
            }
        )

@tarea.get("")
def listar_tareas_endpoint(estado: EstadoTarea | None = None, prioridad: PrioridadTarea | None = None, 
    datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
    
    usuario_id, jti = datos_token

    

    try:
        valido, resultado = buscar_tareas(usuario_id, db, estado, prioridad)

        if valido:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ok",
                    "message": resultado
                }
            )

        else:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "error",
                    "message": []
                }
            )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Error de integracion en la BD"
            }
        )

@tarea.get("/{id_tarea}")
def listar_tarea_endpoint(id_tarea: int, datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_id, jti = datos_token

    try:
        valido, resultado = buscar_tarea(id_tarea, usuario_id, db)

        if valido:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ok",
                    "message": resultado
                }
            )

        else:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": resultado
                }
            )

    except Exception:
        return JSONResponse(
            status=500,
            content={
                "status": "error",
                "message": "Error de integracion en la BD"
            }
        )

@tarea.put("/{id_tarea}")
def actualizar_tarea_endpoint(id_tarea: int, tarea: UpdateTask, datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_id, jti = datos_token

    try:
        valido, resultado = actualizar_tarea(usuario_id, id_tarea, tarea, db)

        if valido:
            return JSONResponse(
                status_code= 200,
                content={
                    "status": "ok",
                    "message": resultado
                }
            )

        else:
            return JSONResponse(
                status_code= 404,
                content={
                    "status": "error",
                    "message": resultado
                }
            )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Error de integracion en la BD"
            }
        )

@tarea.delete("/{id_tarea}")
def eliminar_tarea_endpoint(id_tarea: int, datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
    usuario_id, jti = datos_token

    try:
        valido, resultado = eliminar_tarea(id_tarea, usuario_id, db)

        if valido:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ok",
                    "message": resultado
                }
            )

        else:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": resultado
                }
            )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Error de integracion en la BD"
            }
        )
