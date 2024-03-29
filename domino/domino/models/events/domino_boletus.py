
import uuid
from datetime import date
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint
from sqlalchemy.sql.sqltypes import String, Integer, Date, Boolean, Text, DateTime, Float
from ...config.db import Base
from sqlalchemy.orm import relationship

def generate_uuid():
    return str(uuid.uuid4())

class DominoBoletus(Base):
    """DominoBoletus Class contains standard information for  Domino Boletus at Rounds. Es una boleta por cada mesa"""
 
    __tablename__ = "domino_boletus"
    __table_args__ = {'schema' : 'events'}
    
    id = Column(String, primary_key=True, default=generate_uuid)
    tourney_id = Column(String, ForeignKey("events.tourney.id"), nullable=False)
    round_id = Column(String, ForeignKey("events.domino_rounds.id"), nullable=False)
    table_id = Column(String, ForeignKey("events.domino_tables.id"), nullable=False)
    is_valid = Column(Boolean, nullable=False, default=True)
    status_id  = Column(Integer, ForeignKey("resources.entities_status.id"), nullable=False)
    can_update  = Column(Boolean)
    
    motive_closed  = Column(String)
    motive_closed_description  = Column(String)
    motive_not_valid  = Column(String)
    motive_not_valid_description  = Column(String)
    
    boletus_position = relationship("DominoBoletusPosition")
    boletus_pairs = relationship("DominoBoletusPairs")
    boletus_data = relationship('DominoBoletusData', back_populates="boletus")
    
    tourney = relationship('Tourney')
    
    rounds = relationship('DominoRounds')
    tables = relationship('DominoTables')
    status = relationship("StatusElement")
    
    def dict(self):
        return {
            "id": self.id,
            "tourney_id": self.tourney_id,
            "round_id": self.round_id,
            "table_id": self.table_id,
            "player_id": self.player_id,
            "is_valid": self.is_valid,
            }
 
class DominoBoletusPairs(Base):
    """DominoBoletusPairs Class contains standard information for  Domino Pairs at Rounds. Es una boleta por cada pareja"""
 
    __tablename__ = "domino_boletus_pairs"
    __table_args__ = {'schema' : 'events'}
    
    boletus_id = Column(String, ForeignKey("events.domino_boletus.id"), primary_key=True)
    pairs_id = Column(String, ForeignKey("events.domino_rounds_pairs.id"), primary_key=True)
    is_initiator = Column(Boolean, nullable=False, default=False)
    is_winner = Column(Boolean, nullable=False, default=False)
    positive_points = Column(Integer)
    negative_points = Column(Integer)
    penalty_points = Column(Integer)
    start_date =  Column(DateTime, nullable=False, default=datetime.now())
    end_date =  Column(DateTime, nullable=False, default=datetime.now())
    duration = Column(Float)  # tiempo en minutos,, despues tengo que ver el tipo  de datos
    
    pair = relationship('DominoRoundsPairs')
    
    def dict(self):
        return {
            "boletus_id": self.boletus_id,
            "pairs_id": self.pairs_id,
            "is_initiator": self.is_initiator,
            "is_winner": self.is_winner,
            "positive_points": self.positive_points,
            "negative_points": self.negative_points,
            "duration": self.duration,
            }
               
class DominoBoletusPosition(Base):
    """DominoBoletusPosition Class contains standard information for  Domino Positions at Rounds. 4 posicioones por cada boleta"""
 
    __tablename__ = "domino_boletus_position"
    __table_args__ = {'schema' : 'events'}
    
    boletus_id = Column(String, ForeignKey("events.domino_boletus.id"), primary_key=True)
    position_id = Column(Integer, primary_key=True)
    single_profile_id = Column(String)
    scale_number = Column(Integer) 
    pairs_id = Column(String)
    
    positive_points = Column(Integer) 
    negative_points = Column(Integer) 
    penalty_points = Column(Integer) 
    
    is_winner = Column(Boolean) 
    expelled = Column(Boolean)
    is_guilty_closure = Column(Boolean) 
    
    def dict(self):
        return {
            "boletus_id": self.boletus_id,
            "position_id": self.position_id,
            "single_profile_id": self.single_profile_id,
            "scale_number": self.scale_number,
            "is_winner": self.is_winner,
            "expelled": self.expelled,
            "positive_points": self.positive_points,
            "negative_points": self.negative_points,
            "penalty_points": self.penalty_points,
            }

