from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from ..models.users import UserTable
from ..database import get_db
from .security import verify_password

async def validate_user(username: str, password: str, db: AsyncSession) -> Optional[UserTable]:
    try:
        result =  await db.execute(select(UserTable).where(UserTable.username == username))
        user = result.scalar_one_or_none()
        if not user:
            return None
        
        if user.is_deleted:
            return None
        
        validate_password = verify_password(password=password, hashed_password=user.password_hashed)
        if not validate_password:
            return None
                
        return user
    
    except Exception as e:
        return None