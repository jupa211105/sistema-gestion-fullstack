from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioPut
from app.services.usuarios import crear_usuario, login_usuario, obtener_usuarios, obtener_usuario, actualizar_usuario, eliminar_usuario
from app.services.tokens import revocar_token
from app.dependencies.auth import verificar_token

router = APIRouter(prefix="/usuarios")

@router.post("")
def crear_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
   try:
      resultado = crear_usuario(usuario, db)

      return JSONResponse(
         status_code=201,
         content={
            "message": resultado   
         }
      )

   except Exception:
      return JSONResponse(
         status_code=409,
         content={
            "message": "Correo Ingresado ya existe"
         }    
      )


@router.post("/login")
def iniciar_usuario_endpoint(usuario: UsuarioLogin, db: Session = Depends(get_db)):
   try:
      valido, resultado = login_usuario(usuario, db)

      if valido:
         return JSONResponse( 
            status_code=200,
            content={
               "status": "ok",
               "message": "Usuario iniciado session",
               "token": resultado
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


@router.post("/logout")
def cerrar_session(datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
   usuario_id, jti = datos_token

   valido = revocar_token(jti, db)

   if valido:
      return JSONResponse(
         status_code=200,
         content={
            "status": "ok",
            "message": "Session cerrada correctamente"   
         }
      )



@router.get("")
def listar_usuarios(datos_token = Depends(verificar_token), db: Session = Depends(get_db)):

   usuario_id, jti = datos_token
   try:
      valido, resultado = obtener_usuarios(db)

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

@router.get("/{user_id}")
def listar_usuario(user_id: int, datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
   usuario_id, jti = datos_token

   try:
      valido, resultado = obtener_usuario(user_id, db)

      if valido:
         return JSONResponse(
            status_code = 200,
            content={
               "status": "ok",
               "message": resultado
            }
         )

      else:
         return JSONResponse(
            status_code = 404,
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

@router.put("/{id}")
def modificar_usuario(id: int, usuario: UsuarioPut, datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
   usuario_id, jti = datos_token

   if usuario_id == id:
      try:
         valido, resultado = actualizar_usuario(id, usuario, db)

         if valido:
            return JSONResponse(
               status_code=200,
               content={
                  "status": "ok",
                  "message": "Usuario actualizado correctamente",
                  "ID": resultado
               }
            )

         else:
            return JSONResponse(
               status_code= 404,
               content={
                  "status": "error",
                  "message": "Usuario no encontrado"
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
   
   else:
      return JSONResponse(
         status_code=403,
         content={
            "status": "error",
            "message": "Solo Puedes modificar tu propio perfil"
         }
      )

@router.delete("/{id}")
def borrar_usuario(id: int, datos_token = Depends(verificar_token), db: Session = Depends(get_db)):
   usuario_id, jti = datos_token

   if usuario_id == id:

      try:
         valido, resultado = eliminar_usuario(id, db)

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

   else:
      return JSONResponse(
         status_code=403,
         content={
            "status": "error",
            "message": "Solo puedes eliminar tu propio usuario"
         }
      )







   
      
      

      
      
