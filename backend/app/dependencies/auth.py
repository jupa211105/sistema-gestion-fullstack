import os
from  uuid import uuid4 
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from app.database import get_db
from app.services.tokens import token_revocado

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

 
def crear_token(usuario_id):
    ahora = datetime.now(timezone.utc)

    payload = {
        "sub": str(usuario_id),
        "jti": str(uuid4()),
        "exp": ahora + timedelta(minutes=EXPIRE_MINUTES)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token



def verificar_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")
        jti = payload.get("jti")

        
        if usuario_id is None:
            raise HTTPException(
                status_code=401,
                detail="Se requiere un token para acceder a este recurso"
            )

        if not isinstance(usuario_id, str):
            raise HTTPException(
                status_code=401,
                detail="El formato encontrado no es el correctto"
            )

        if jti is None:
            raise HTTPException(
                status_code=401,
                detail="El token no contiene JTI"
            )

        if token_revocado(jti,db):
            raise HTTPException(
                status_code=401,
                detail="El token ha sido revocado"
            )

        try:
            usuario_id = int(usuario_id)
                                     
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="El formato debe ser un numero entero"
            )

        return usuario_id, jti

    except  ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail= "El token ha expirado"
        )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )
