from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from .config import settings

Base = declarative_base() # base declarativa para la creacion de tablas

DATABASE_URL = settings.database_url


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
