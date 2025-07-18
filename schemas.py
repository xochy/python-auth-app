from pydantic import BaseModel, EmailStr

# Esquema base para usuario (atributos comunes)
class UserBase(BaseModel):
    username: str
    email: EmailStr # Valida que sea un formato de correo electrónico

# Esquema para crear un nuevo usuario (incluye la contraseña)
class UserCreate(UserBase):
    password: str

# Esquema para la respuesta de usuario (NO incluye la contraseña hasheada)
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True # Permite que Pydantic lea datos directamente de un modelo ORM

# Esquema para el inicio de sesión
class UserLogin(BaseModel):
    username: str
    password: str

# Esquema para el token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para los datos del token
class TokenData(BaseModel):
    username: str | None = None