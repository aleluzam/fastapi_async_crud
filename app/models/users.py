from sqlalchemy import Column, Boolean, String, Integer
from ..database import Base
from ..models.mixins import TimestampMixin, SoftDeleteMixin


class UserTable(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    mail = Column(String(50), unique=True, nullable=False)
    password_hashed = Column(String(250), nullable = False)