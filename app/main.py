from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from .database import create_tables, async_engine, get_db, drop_tables
from .models.users import UserTable
from .schemas.users import UserPublic
from .models.comments import CommentTable
from .models.posts import PostTable
from .models.tags import TagTable
from .utils.security import verify_password, get_current_user
from .schemas.tokens import VerifyPassword

from .routes.auth import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
     # await create_tables()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)

#routers
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/users")  
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserTable))
    users = result.scalars().all()
    return users

@app.get("/comments")  
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CommentTable))
    users = result.scalars().all()
    return users

@app.get("/posts")  
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PostTable))
    users = result.scalars().all()
    return users

@app.get("/tags")  
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TagTable))
    users = result.scalars().all()
    return users


@app.post("/add_user")
async def add_user(db: AsyncSession = Depends(get_db)):
    new_user = UserTable(
        username="luzardoaa",
        mail="alzzlaa22@gmail.com",
        password_hashed = "$argon2id$v=19$m=65536,t=4,p=2$4CuJLUm07ptieuBsHrFm5Q==$NQa29NW6tpz68WhnYnFex4fiA1ZUFnqqVyMY5Ag58l0="
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

@app.get("/security", response_model=UserPublic)
async def protected(user: UserPublic = Depends(get_current_user)):
        return f"Hola {user.username}, esta ruta esta protegida"


