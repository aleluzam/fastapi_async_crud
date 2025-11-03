from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

Base = declarative_base() #base a heredar para la creacion de las tablas

DATABASE_URL = settings.database_url # se importa desde la instancia de la clase que creamos


# motor asyncrono de coneccion a base de datos
async_engine = create_async_engine(DATABASE_URL,
                                   echo=True ) # enseña los comandos sql en la terminal 


# Creador de sesiones
AsyncSessionLocal = async_sessionmaker( 
    async_engine,
    class_=AsyncSession, expire_on_commit= False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)