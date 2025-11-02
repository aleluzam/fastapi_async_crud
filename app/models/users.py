from ..database import Base
from sqlalchemy import Column, Boolean, String, Integer


class UserTable(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, nullable = True)
    last_name = Column(String(200), index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    mail = Column(String(50), unique=True, nullable=False)
    active = Column(Boolean, default=True)