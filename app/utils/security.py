from pwdlib import PasswordHash
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from datetime import timedelta, datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..config import settings
from ..database import get_db
from ..models.users import UserTable
from ..schemas.users import UserPublic


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# hashing
password_hash = PasswordHash.recommended()

def hash_password(password):
    return password_hash.hash(password)

def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)


#jwt
def encode_jwt(payload: dict):
    
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary")
    if not SECRET_KEY:
        return ValueError("SECRET_KEY not configured")
    
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    
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
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="System internal error"
        )

# authorization
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials cant be validated",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode_jwt(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    data = await db.execute(select(UserTable).where(UserTable.username == username))
    user = data.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    user = UserPublic.model_validate(user)
    
    return user