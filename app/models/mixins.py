from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func


class TimestampMixin:
    created_at = Column(DateTime, default = func.now(), nullable = False)
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default = False, nullable = False)
    deleted_at = Column(DateTime, nullable = True)
    
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = func.now()
        
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        
    