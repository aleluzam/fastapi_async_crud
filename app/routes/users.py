from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..crud.base import CRUDBase
from ..models.users import UserTable
from ..utils.security import get_current_user
from ..schemas.users import UserPublic, UserUpdate, UserResponse, UserCreate



users_router = APIRouter(prefix="/user", tags=["users"])

crud_users = CRUDBase(UserTable)

######## GET #########
@users_router.get("/all")
async def get_all_users(db: AsyncSession = Depends(get_db)):
    all_users = await crud_users.get_all(db=db)
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No hay usuarios actualmente")
    return all_users

@users_router.get("/{id}")
async def get_by_id(id: int, db: AsyncSession = Depends(get_db), current_user: UserPublic = Depends(get_current_user)):
    user = await crud_users.get_by_id(id=id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Registro de id {id} no encontrado")
    return user

# POST
@users_router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    new_user = await crud_users.create(db=db, new_obj=user)
    return new_user

# PUT
@users_router.put("/update/{id}", response_model=UserPublic)
async def update_user(id: int, update_user: UserUpdate, db: AsyncSession = Depends(get_db)) -> UserPublic:
    updated_user = await crud_users.update(db=db, updt_obj=update_user, id=id)
    return updated_user



# DELETE
@users_router.delete("/delete/{id}")
async def soft_delete(id: int, db: AsyncSession = Depends(get_db)):
    obj_to_eliminate = await crud_users.soft_delete(db=db, id=id)
    return obj_to_eliminate