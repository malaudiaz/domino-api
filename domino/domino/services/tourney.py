import math
import uuid
from typing import List
from datetime import datetime
from fastapi import HTTPException, Request
from unicodedata import name
from fastapi import HTTPException
from domino.models.tourney import Tourney
from domino.schemas.tourney import TourneyBase, TourneySchema, TourneyCreated
from domino.schemas.result_object import ResultObject, ResultData
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from domino.auth_bearer import decodeJWT
from domino.functions_jwt import get_current_user
from domino.services.status import get_one_by_name, get_one as get_one_status
from domino.app import _
from domino.services.utils import get_result_count
from domino.services.event import get_one as get_one_event, get_all as get_all_event
            
def get_all(request:Request, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_from = "FROM events.tourney tou " +\
        "JOIN events.events eve ON eve.id = tou.event_id " +\
        "JOIN resources.entities_status sta ON sta.id = tou.status_id " 
    
    str_count = "Select count(*) " + str_from
    str_query = "Select tou.id, event_id, eve.name as event_name, tou.modality, tou.name, tou.summary, tou.start_date, " +\
        "tou.status_id, sta.name as status_name " + str_from
    
    str_where = " WHERE sta.name != 'CANCELLED' "  
    
    dict_query = {'name': " AND eve.name ilike '%" + criteria_value + "%'",
                  'summary': " AND summary ilike '%" + criteria_value + "%'",
                  'modality': " AND modality ilike '%" + criteria_value + "%'",
                  'start_date': " AND start_date >= '%" + criteria_value + "%'",
                  }
    
    str_count += str_where
    str_query += str_where
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    str_count += dict_query[criteria_key] if criteria_value else "" 
    str_query += dict_query[criteria_key] if criteria_value else "" 
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY start_date " 
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, page, db=db) for item in lst_data]
    
    return result

def create_dict_row(item, page, db: Session):
    
    new_row = {'id': item['id'], 'event_id': item['event_id'], 'event_name': item['event_name'], 'name': item['name'], 
               'modality': item['modality'], 'summary' : item['summary'], 'startDate': item['start_date'] 
               }
       
    if page != 0:
        new_row['selected'] = False
    return new_row

def get_one(tourney_id: str, db: Session):  
    return db.query(Tourney).filter(Tourney.id == tourney_id).first()

def get_one_by_id(tourney_id: str, db: Session): 
    result = ResultObject()  
    result.data = db.query(Tourney).filter(Tourney.id == tourney_id).first()
    return result

def get_all_by_event_id(event_id: str, db: Session): 
    result = ResultObject()  
    
    str_from = "FROM events.tourney tou " +\
        "JOIN events.events eve ON eve.id = tou.event_id " +\
        "JOIN resources.entities_status sta ON sta.id = tou.status_id "
    
    str_query = "Select tou.id, event_id, eve.name as event_name, tou.modality, tou.name, tou.summary, tou.start_date, " +\
        "tou.status_id, sta.name as status_name " + str_from
    
    str_query += " WHERE sta.name != 'CANCELLED' and event_id = '" + str(event_id) + "' ORDER BY start_date "  
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, 0, db=db) for item in lst_data]
    
    return result

def new(request, event_id: str, lst_tourney: List[TourneyCreated], db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    one_status = get_one_by_name('CREATED', db=db)
    if not one_status:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_found"))
    
    one_event = get_one_event(event_id, db=db)
    if one_event.status_id != one_status.id:
        raise HTTPException(status_code=404, detail=_(locale, "event.event_closed"))
    
    for item_to in lst_tourney:
        id = str(uuid.uuid4())
        if item_to.startDate < one_event.start_date: 
            raise HTTPException(status_code=404, detail=_(locale, "tourney.incorrect_startDate"))
        if item_to.startDate > one_event.close_date: 
            raise HTTPException(status_code=404, detail=_(locale, "tourney.incorrect_startDate"))
        
        db_tourney = Tourney(id=id, event_id=event_id, modality=item_to.modality, name=item_to.name, 
                            summary=item_to.summary, start_date=item_to.startDate, 
                            status_id=one_status.id, created_by=currentUser['username'], 
                            updated_by=currentUser['username'])
        db.add(db_tourney)
    
    try:
        
        db.commit()
        result.data = {'event_id': event_id}
        return result
       
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "tourney.error_new_tourney")               
        raise HTTPException(status_code=403, detail=msg)

def delete(request: Request, tourney_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    one_status = get_one_by_name('CANCELLED', db=db)
    if not one_status:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_found"))
    
    try:
        db_tourney= db.query(Tourney).filter(Tourney.id == tourney_id).first()
        if db_tourney:
            db_tourney.status_id = one_status.id
            db_tourney.updated_by = currentUser['username']
            db_tourney.updated_date = datetime.now()
            db.commit()
            return result
        else:
            raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "tourney.imposible_delete"))
    
def update(request: Request, tourney_id: str, tourney: TourneyBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
       
    db_tourney = db.query(Tourney).filter(Tourney.id == tourney_id).first()
    
    if db_tourney:
        
        if db_tourney.status_id == 4:  # FINALIZED
            raise HTTPException(status_code=400, detail=_(locale, "tourney.tourney_closed"))
    
        if tourney.name and db_tourney.name != tourney.name:
            db_tourney.name = tourney.name
        
        if tourney.summary and db_tourney.summary != tourney.summary:    
            db_tourney.summary = tourney.summary
            
        if tourney.modality and db_tourney.modality != tourney.modality:    
            db_tourney.modality = tourney.modality
            
        if tourney.start_date and db_tourney.start_date != tourney.start_date:    
            db_tourney.start_date = tourney.start_date
            
        db_tourney.updated_by = currentUser['username']
        db_tourney.updated_date = datetime.now()
         
        try:
            db.add(db_tourney)
            db.commit()
            db.refresh(db_tourney)
            return result
        except (Exception, SQLAlchemyError) as e:
            print(e.code)
            if e.code == "gkpj":
                raise HTTPException(status_code=400, detail=_(locale, "tourney.already_exist"))
            
    else:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))


