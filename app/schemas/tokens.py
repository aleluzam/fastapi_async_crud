from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    
class VerifyPassword(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=10, max_length=30)

