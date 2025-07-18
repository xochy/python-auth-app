from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# Modelo de usuario para SQLAlchemy (representa la tabla en la DB)
class User(Base):
    __tablename__ = "users" # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True) # Clave primaria, auto-incrementable
    username = Column(String(50), unique=True, index=True) # Nombre de usuario, debe ser único
    email = Column(String(100), unique=True, index=True) # Correo electrónico, debe ser único
    hashed_password = Column(String(255)) # Contraseña hasheada (NO la contraseña en texto plano)

    # Representación de la instancia del objeto cuando se imprime
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"