"""coding=utf-8."""

import uuid
from datetime import date
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, Date, Boolean, Float
from ...config.db import Base
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid.uuid4())

class Inscriptions(Base):
    """Inscriptions Class contains standard information for  Invitations at Event."""
 
    __tablename__ = "inscriptions"
    __table_args__ = {'schema' : 'events'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    tourney_id = Column(String, ForeignKey("events.tourney.id"), nullable=False)
    profile_id = Column(String, ForeignKey("enterprise.profile_member.id"), nullable=False)
    user_id = Column(String)
    modality = Column(String(30), nullable=False) # Individual/Parejas/Equipo/
    was_pay = Column(Boolean)
    payment_way = Column(String(30))
    import_pay = Column(Float)
    status_name  = Column(String, ForeignKey("resources.entities_status.name"), nullable=False)
    created_by = Column(String, ForeignKey("enterprise.users.username"), nullable=False)
    created_date = Column(Date, nullable=False, default=date.today())
    updated_by = Column(String, ForeignKey("enterprise.users.username"), nullable=True)
    updated_date = Column(Date, nullable=False, default=date.today())
    
    tourney = relationship('Tourney')
    
    def dict(self):
        return {
            "id": self.id,
            "tourney_id": self.tourney_id,
            "profile_id": self.profile_id,
            "modality": self.modality,
            "status_name": self.status_name,
            'created_by': self.created_by
            }
