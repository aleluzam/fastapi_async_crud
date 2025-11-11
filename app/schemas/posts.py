from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from models.comments import CommentTable


class PostBase(BaseModel):
    title: str = Field(min_length=10, max_length=50)
    content: str = Field(min_length=10, max_length=200)

class PostCreate(PostBase):
    user_id: int

class PostOnDB(PostBase):
    user_id: str
    created_at: datetime
    updated_at: datetime | None
    is_deleted: bool
    deleted_at: datetime | None

class PostUpdate(BaseModel):
    title: str | None = Field(min_length=10, max_length=50, default = None)
    content: str | None = Field(min_length=10, max_length=200, default = None)

class PostResponse(PostBase):
    created_at: datetime
    updated_at: datetime | None
    # agregar comentarios y tags