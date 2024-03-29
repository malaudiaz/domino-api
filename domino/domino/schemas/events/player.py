"""coding=utf-8."""

from datetime import datetime, date
from pydantic import BaseModel, validator
from typing import Optional
        
class PlayerBase(BaseModel):
    tourney_id: str
    profile_id: str
    nivel: Optional[str]
    invitation_id: Optional[str]
    
    @validator('tourney_id')
    def tourney_id_not_empty(cls, tourney_id):
        if not tourney_id:
            raise ValueError('Identificador del de Torneo es Requerido')
        return tourney_id
    
    @validator('profile_id')
    def profile_id_not_empty(cls, profile_id):
        if not profile_id:
            raise ValueError('Id del profile de usario es Requerido')
        return profile_id
    
class PlayerSchema(PlayerBase):
    
    id: Optional[int]
    is_active: bool = True
    
    created_by: str
    created_date: datetime = datetime.today()
    updated_by: str
    updated_date: datetime = datetime.today()
    
    class Config:
        orm_mode = True

class PlayerRegister(BaseModel):
    
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    alias: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    city_id: Optional[int]
    country_id: Optional[int]
    elo: Optional[float]
    level: Optional[str]
    
    club_id: Optional[int]
    federation_id: Optional[int]
    
class PlayerUpdatedRegister(BaseModel):
    
    name: str
    email: Optional[str]
    elo: Optional[float]
    level: Optional[str]
    
    @validator('name')
    def name_not_empty(cls, name):
        if not name:
            raise ValueError('Nombre del Jugador es Requerido')
        return name
    
    @validator('email')
    def email_not_empty(cls, email):
        if not email:
            raise ValueError('Dirección de Correo es Requerida')
        return email
    
class PlayerEloBase(BaseModel):
    
    profile_id: str
    elo: float
    
    @validator('elo')
    def elo_not_empty(cls, elo):
        if not elo:
            raise ValueError('Valor de Elo es requerido')
        return elo
    