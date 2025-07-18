import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv() # Carga las variables de entorno del archivo .env

DATABASE_URL = os.getenv("DATABASE_URL")

# 1. create_async_engine: Crea una instancia del motor de base de datos.
#    future=True: Usa la API 2.0 de SQLAlchemy para operaciones asíncronas.
#    echo=True: Opcional, muestra las sentencias SQL en la consola para depuración.
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# 2. sessionmaker: Crea una "fábrica" de sesiones. Cada sesión será un "espacio de trabajo"
#    para tus operaciones de base de datos.
#    autocommit=False, autoflush=False: Evita que las operaciones se confirmen
#    o se vacíen automáticamente en la base de datos. Necesitarás hacer commit explícitamente.
#    bind=engine: Asocia esta fábrica de sesiones con nuestro motor.
#    class_=AsyncSession: Indica que las sesiones serán asíncronas.
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# 3. declarative_base: Retorna una clase base para tus modelos ORM.
#    Todas tus tablas (modelos) heredarán de esta clase.
Base = declarative_base()

# Función para obtener una sesión de base de datos.
# Esto se usará como una dependencia en FastAPI.
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session # Provee la sesión al código que la llama
        finally:
            await session.close() # Asegura que la sesión se cierre al finalizar