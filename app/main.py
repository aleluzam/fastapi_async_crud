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
from .routes.users import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
     # await create_tables()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)

#routers
app.include_router(auth_router)
app.include_router(users_router)



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/security", response_model=str)
async def protected(user: UserPublic = Depends(get_current_user)):
        return f"Hola {user.username}, esta ruta esta protegida"


