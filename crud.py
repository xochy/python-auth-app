from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

import models, schemas
from auth import get_password_hash # Importamos la función para hashear contraseñas

# Función para obtener un usuario por nombre de usuario
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(models.User).filter(models.User.username == username)
    )
    return result.scalars().first()

# Función para obtener un usuario por email
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(models.User).filter(models.User.email == email)
    )
    return result.scalars().first()

# Función para crear un nuevo usuario
async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password) # Hasheamos la contraseña
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user) # Agrega el nuevo usuario a la sesión
    await db.commit() # Confirma los cambios en la base de datos
    await db.refresh(db_user) # Refresca el objeto para obtener el ID generado
    return db_user

# Función para eliminar un usuario
async def delete_user(db: AsyncSession, user_id: int):
    await db.execute(
        delete(models.User).where(models.User.id == user_id)
    )
    await db.commit()