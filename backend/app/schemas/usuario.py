from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    password: str


class UsuarioLogin(BaseModel):
    correo: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class UsuarioPut(BaseModel):
    nombre: str
    correo: str