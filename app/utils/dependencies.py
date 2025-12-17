from fastapi import Depends, HTTPException, status
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from ..models.users import UserTable
from ..database import get_db
from .security import verify_password, get_current_user, oauth2_scheme
from ..config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

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
    
    
async def get_id_from_jwt(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: falta ID de usuario",
                headers={"WWW-Authenticate": "Bearer"}
            )
        result = await db.execute(select(UserTable).where(UserTable.id == int(user_id)))
        existe_id = result.scalar_one_or_none()
        if not existe_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Registro de id {user_id} no encontrado",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return int(user_id)
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired, login again",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials cant be validated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except HTTPException: 
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="System internal error"
        )

