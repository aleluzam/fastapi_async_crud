from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from .database import async_engine
from .schemas.users import UserPublic
from .utils.security import  get_current_user
from .routes.auth import auth_router
from .routes.users import users_router
from .middleware import calculate_process_time


@asynccontextmanager
async def lifespan(app: FastAPI):
     # await create_tables()
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan, title="Async FastAPI Crud")

app.middleware("http")(calculate_process_time)

#routers
app.include_router(auth_router)
app.include_router(users_router)



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/security", response_model=str)
async def protected(user: UserPublic = Depends(get_current_user)):
        return f"Hola {user.username}, esta ruta esta protegida"


