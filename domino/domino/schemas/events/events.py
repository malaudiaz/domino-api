"""coding=utf-8."""
 
from datetime import datetime, date
from pydantic import BaseModel, validator
from typing import Optional, List
# class EventBase(BaseModel):
#     name: Optional[str]
#     summary: Optional[str]
#     city_id: Optional[int]
#     main_location: Optional[str]
    
#     start_date: Optional[date] = date.today()
#     close_date: Optional[date] = date.today()
    
#     # tourney: Optional[str]
    
#     @validator('name')
#     def name_not_empty(cls, name):
#         if not name:
#             raise ValueError('Nombre de Evento es Requerido')
#         return name
    
#     @validator('city_id')
#     def city_id_id_not_empty(cls, city_id):
#         if not city_id:
#             raise ValueError('Ciudad del Evento es Requerida')
#         return city_id
    
# class EventSchema(EventBase):
#     id: Optional[int]
    
#     status_id: int
#     created_by: str
#     created_date: datetime = datetime.today()
#     updated_by: str
#     updated_date: datetime = datetime.today()
    
#     class Config:
#         orm_mode = True
        
# class EventFollowers(BaseModel):
#     event_id: str
       
#     @validator('event_id')
#     def event_id_not_empty(cls, event_id):
#         if not event_id:
#             raise ValueError('ID de Event Requerido')
#         return event_id