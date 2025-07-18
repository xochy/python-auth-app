from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from datetime import timedelta

import schemas, crud, models
from database import engine, Base, get_db
from auth import create_access_token, verify_password, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Inicializa la aplicación FastAPI
app = FastAPI(title="API de Autenticación de Usuarios")

# Esquema de seguridad para OAuth2 con el flujo de contraseña
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para crear las tablas en la base de datos al iniciar la aplicación
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Crea todas las tablas definidas en Base (nuestro models.py)
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas de la base de datos creadas/actualizadas.")

# --- RUTAS DE AUTENTICACIÓN ---

# Ruta para registrar un nuevo usuario (Sign Up)
@app.post("/signup", response_model=schemas.UserResponse, summary="Registrar un nuevo usuario")
async def signup(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user_by_username = await crud.get_user_by_username(db, username=user.username)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado.")

    db_user_by_email = await crud.get_user_by_email(db, email=user.email)
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")

    return await crud.create_user(db=db, user=user)

# Ruta para iniciar sesión y obtener un token (Sign In)
@app.post("/token", response_model=schemas.Token, summary="Iniciar sesión y obtener token JWT")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dependencia para obtener el usuario actual a partir del token JWT
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = decode_access_token(token)
    if username is None:
        raise credentials_exception
    user = await crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Ruta de ejemplo para verificar el usuario autenticado (requiere token)
@app.get("/users/me/", response_model=schemas.UserResponse, summary="Obtener información del usuario actual")
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Ruta para cerrar sesión (Sign Out) - en una API stateless, "cerrar sesión"
# es simplemente dejar de usar el token. No hay una "sesión" activa en el servidor.
# Esta ruta es más para informar al cliente que el token ya no debe usarse.
@app.post("/signout", summary="Cerrar sesión (Invalidar token JWT en el cliente)")
async def signout(current_user: models.User = Depends(get_current_user)):
    return {"message": "Sesión cerrada. El token ya no debe usarse."}