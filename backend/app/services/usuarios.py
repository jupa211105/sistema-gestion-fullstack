from app.models.usuario import Usuario
from app.services.seguridad import generar_hash, verificar_password
from app.dependencies.auth import crear_token

def crear_usuario(usuario, db):
    try:
        nuevo_usuario = Usuario(
            nombre= usuario.nombre,
            correo= usuario.correo,
            password_hash=generar_hash(usuario.password)
        )

        db.add(nuevo_usuario)
        db.commit()

        return nuevo_usuario.id

    except Exception:
        db.rollback()
        raise



def login_usuario(usuario, db):
    correo = usuario.correo
    password = usuario.password

    try:
        resultado = db.query(Usuario).filter_by(correo=correo).first()

        if resultado:
            password_hash = resultado.password_hash

            valido = verificar_password(password, password_hash)
            

            if valido:
                id = resultado.id
                token = crear_token(id)
                
                return True, token

            else:
               return False, "Contraseña Incorrecta"

        else:
           return False, "Correo no encontrado"

    except Exception:
        raise


def obtener_usuarios(db):
    try:
        resultado = db.query(Usuario).all()
 
        if resultado:
            usuarios = [
                {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                }
                for usuario in resultado
            ]

            return True, usuarios

        else:
            return False, "Usuario no encontrado"

    except Exception:
        raise

def obtener_usuario(user_id, db):
    try:
        resultado = db.query(Usuario).filter_by(id=user_id).first()

        if resultado:
            usuario = {
                "id": resultado.id,
                "nombre": resultado.nombre,
                "correo": resultado.correo
            }

            return True, usuario

        else:
            return False, "Usuario no encontrado"

    except Exception:
        raise

def actualizar_usuario(id, usuario, db):
    try:
        resultado = db.query(Usuario).filter_by(id=id).first()

        if resultado:
            resultado.correo = usuario.correo
            resultado.nombre = usuario.nombre
        
            db.commit()

            return True, resultado.id

        else:
            return False, "Usuario no encontrado"

    except Exception:
        db.rollback()
        raise

def eliminar_usuario(id, db):
    try:
        usuario = db.query(Usuario).filter_by(id=id).first()

        if usuario:
            db.delete(usuario)
            db.commit()

            return True, "Usuario eliminado correctamente"


        else:
            return False, "Usuario no encontrado"

    except Exception:
        db.rollback()
        raise


    



          
