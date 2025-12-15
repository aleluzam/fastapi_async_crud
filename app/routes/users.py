from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..crud.base import CRUDBase
from ..models.users import UserTable
from ..utils.security import get_current_user
from ..schemas.users import UserPublic



users_router = APIRouter(prefix="/user", tags=["users"])

crud_users = CRUDBase(UserTable)


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

