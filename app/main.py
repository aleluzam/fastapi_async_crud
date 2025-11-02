from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from .database import create_tables, async_engine, get_db
from .models import users
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models.users import UserTable




@asynccontextmanager # manejo del ciclo de vida
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


from sqlalchemy import select

@app.get("/users")  
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable))
    users = result.scalars().all()
    return users
    
    
@app.post("/add_user")
async def add_user(db: AsyncSession = Depends(get_db)):
    new_user = UserTable(
        name="Alejandro",
        last_name="Luzardo",
        username="aleluzam",
        mail="alzzla@gmail.com"
    )
    db.add(new_user)
    await db.commit() 
    await db.refresh(new_user)
    
    return {
        "message": "Se ha agregado correctamente",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "mail": new_user.mail
        }
    }
