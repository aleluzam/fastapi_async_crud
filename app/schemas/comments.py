from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from schemas.users import UserPublic


class CommentBase(BaseModel):
    author: UserPublic
    content: str = Field(max_length=200)

class CommentCreate(BaseModel):
    post_id: int
    user_id: int
    content: str = Field(max_length=200)

class CommentUpdate(BaseModel):
    content: str | None = None

class CommentResponse(CommentBase):
    author: UserPublic