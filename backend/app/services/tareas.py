from app.models.tareas import Tarea


def validar_estado_prioridades(tarea):
    estado = tarea.estado
    prioridad = tarea.prioridad

    if estado not in ["pendiente", "en_progreso", "completada"]:
        return "El estado debe estar en pendiente, en_progreso o completada"

    if prioridad not in ["baja", "media", "alta"]:
        return "La prioridad debe estar en baja, media o alta"

    else:
        return None

def crear_tarea(tarea, usuario_id, db):
    error = validar_estado_prioridades(tarea)

    if error:
        return False, error

    try:
        nueva_tarea = Tarea(
            titulo = tarea.titulo,
            descripcion = tarea.descripcion,
            estado = tarea.estado,
            prioridad= tarea.prioridad,
            usuario_id = usuario_id
        )

        db.add(nueva_tarea)
        db.commit()

        return True, nueva_tarea.id

    except Exception:
        db.rollback()
        raise


def buscar_tareas(usuario_id, db, estado, prioridad):
    try:
        consulta = db.query(Tarea).filter_by(usuario_id=usuario_id)

        


        if estado:
            consulta = consulta.filter_by(estado=estado)

        if prioridad:
            consulta = consulta.filter_by(prioridad=prioridad)

        resultado = consulta.all()

        if resultado:
            tareas = [
                {
                    "id": campo.id,
                    "titulo": campo.titulo,
                    "descripcion": campo.descripcion,
                    "estado": campo.estado,
                    "prioridad": campo.prioridad,
                    "usuario_id": campo.usuario_id,
                    "fecha_creacion": str(campo.fecha_creacion) 
                }
                for campo in resultado
            ]

            return True, tareas

        else:
            return False

    except Exception:
        raise


def buscar_tarea(id_tarea, usuario_id, db):
    try:
        resultado = db.query(Tarea).filter_by(id=id_tarea, usuario_id=usuario_id).first()

        if resultado:
            tarea = {
                        "id": resultado.id,
                        "titulo": resultado.titulo,
                        "descripcion": resultado.descripcion,
                        "estado": resultado.estado,
                        "prioridad": resultado.prioridad,
                        "usuario_id": resultado.usuario_id,
                        "fecha_creacion": str(resultado.fecha_creacion)
                    }
                

            return True, tarea

        else:
            return False, "Tarea no encontrada"

    except Exception:
        raise


def actualizar_tarea(usuario_id, id_tarea, tarea, db):
    try:
        resultado = db.query(Tarea).filter_by(id=id_tarea, usuario_id=usuario_id).first()

        if resultado:
            resultado.titulo = tarea.titulo
            resultado.descripcion = tarea.descripcion
            resultado.estado = tarea.estado
            resultado.prioridad = tarea.prioridad

            
            db.commit()

            return True, "Tarea actualizada correctamente"

        else:
            return False, "Tarea no encontrada"

    except Exception:
        db.rollback()
        raise

def eliminar_tarea(id_tarea, usuario_id, db):
    try:
        resultado = db.query(Tarea).filter_by(id=id_tarea, usuario_id=usuario_id).first()

        if resultado:
            db.delete(resultado)
            db.commit()

            return True, "Tarea eliminada correctamente"

        else:
            return False, "Tarea no encontrada"

    except Exception:
        db.rollback()
        raise