from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional

from ..utils.dependencies import validate_user
from ..utils.security import encode_jwt, hash_password
from ..config import settings
from ..database import get_db
from ..schemas.tokens import Token
from ..schemas.users import UserCreate, UserResponse, UserLogin
from ..models.users import UserTable


auth_router = APIRouter(prefix="/auth", tags=["authentication"])



@auth_router.get("/hola")
async def hello_from_auth():
    return "Hello from auth"


@auth_router.post("/token", response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> Token:
    
    user =  await validate_user(password=form_data.password, username=form_data.username, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    }
    
    try:
        access_token = encode_jwt(payload)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )

    return Token(access_token=access_token, token_type="bearer")



# register
@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    result = await db.execute(select(UserTable).where(or_(UserTable.username == user.username, UserTable.mail == user.mail)))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mail already registered"
            )

    try:
        new_hashed_password = hash_password(user.password)
        
        new_user = UserTable(
            username = user.username,
            password_hashed = new_hashed_password,
            mail = user.mail
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return UserResponse.model_validate(new_user)
    
    except Exception as e:
        await db.rollback()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )



# login
@auth_router.post("/login", response_model=Token)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)) -> Token:
    
    user = await validate_user(password=data.password, username=data.username, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    }
    
    try:
        access_token = encode_jwt(payload)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )

    return Token(access_token=access_token, token_type="bearer")


