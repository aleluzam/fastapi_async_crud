from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.dependencies import validate_user
from ..utils.security import encode_jwt
from ..config import settings
from ..database import get_db
from ..schemas.tokens import Token


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