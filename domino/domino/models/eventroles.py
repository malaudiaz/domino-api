"""coding=utf-8."""

from email.policy import default
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import String, DateTime, Integer
from ..config.db import Base

class EventRoles(Base):
    """EventRoles Class contains standard information for a Event Roles."""
 
    __tablename__ = "event_roles"
    __table_args__ = {'schema' : 'resources'}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(100), nullable=False)
    created_by = Column(String(50), nullable=False, default='foo')
    created_date = Column(DateTime, nullable=False, default=datetime.now())
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by,
            "created_date": self.created_date
        }