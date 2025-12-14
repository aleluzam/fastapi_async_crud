from fastapi import APIRouter


users_router = APIRouter(prefix="/user", tags=["users_routes"])



@users_router.get("/hello")
async def hello():
    return "Hello from users"


