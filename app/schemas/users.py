from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    mail: EmailStr

class UserPublic(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(min_length=10, max_length=30)
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("La contraseña debe tener al menos un número")
        if not any(char.isupper() for char in v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        special_chars = "!@#$%^&*()_+-=[]{|};:,.<>?"
        if not any(char in special_chars for char in v):
            raise ValueError("La contraseña debe contener al menos un caracter especial")
        return v

class UserUpdate(BaseModel):
    username: str | None = Field(min_length=5, max_length=50, default=None)
    mail: EmailStr | None = None


class UserInDB(UserBase):
    password_hashed: str
    id: int
    created_at: datetime
    updated_at: datetime | None
    is_deleted: bool
    deleted_at: datetime | None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime | None
    
    model_config = ConfigDict(from_attributes=True)