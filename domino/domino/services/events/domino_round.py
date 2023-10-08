import math
import uuid

from datetime import datetime
from fastapi import HTTPException, Request, UploadFile, File
from unicodedata import name
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
import json
from domino.auth_bearer import decodeJWT
from domino.functions_jwt import get_current_user
from domino.config.config import settings
from domino.app import _
from fastapi.responses import FileResponse
from os import getcwd

from domino.models.events.domino_tables import DominoTables
from domino.models.events.tourney import Tourney
from domino.models.events.tourney import Tourney, SettingTourney

from domino.schemas.events.tourney import TourneyCreated, SettingTourneyCreated
from domino.schemas.events.events import EventBase, EventSchema
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.resources.status import get_one_by_name as get_one_status_by_name, get_one as get_one_status
from domino.services.enterprise.users import get_one_by_username

from domino.services.resources.utils import get_result_count, upfile, create_dir, del_image, get_ext_at_file, remove_dir
from domino.services.enterprise.userprofile import get_one as get_one_profile
            
def get_all(request:Request, profile_id:str, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    api_uri = str(settings.api_uri)
    
    str_from = "FROM events.events eve " +\
        "JOIN resources.entities_status sta ON sta.id = eve.status_id " +\
        "JOIN resources.city city ON city.id = eve.city_id " +\
        "JOIN resources.country country ON country.id = city.country_id " 
        
    str_count = "Select count(*) " + str_from
    str_query = "Select eve.id, eve.name, start_date, close_date, registration_date, registration_price, city.name as city_name, " +\
        "main_location, summary, image, eve.status_id, sta.name as status_name, country.id as country_id, city.id  as city_id, " +\
        "eve.profile_id as profile_id " + str_from
    
    str_where = " WHERE sta.name != 'CANCELLED' "  
    
    if profile_id:
        str_where += "AND profile_id = '" + profile_id + "' "
    # debo incluir los de los perfiles que el sigue
    
    dict_query = {'name': " AND eve.name ilike '%" + criteria_value + "%'",
                  'summary': " AND summary ilike '%" + criteria_value + "%'",
                  'city_name': " AND city_name ilike '%" + criteria_value + "%'",
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
    
    str_query += " ORDER BY start_date DESC " 
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, page, db=db, incluye_tourney=True, api_uri=api_uri) for item in lst_data]
    
    return result

def create_dict_row(item, page, db: Session, incluye_tourney=False, api_uri=""):
    
    image = api_uri + "/api/image/" + str(item['profile_id']) + "/" + item['id'] + "/" + item['image']
    
    new_row = {'id': item['id'], 'name': item['name'], 
               'startDate': item['start_date'], 'endDate': item['close_date'], 
               'country': item['country_id'], 'city': item['city_id'],
               'city_name': item['city_name'], 'campus': item['main_location'], 
               'summary' : item['summary'],
               'photo' : image, 'tourney':[]}
    if page != 0:
        new_row['selected'] = False
    
    return new_row

def get_one(table_id: str, db: Session):  
    return db.query(DominoTables).filter(DominoTables.id == table_id).first()

def get_one_by_id(table_id: str, db: Session): 
    result = ResultObject()  
    
    api_uri = str(settings.api_uri)
    
    one_table = get_one(table_id, db=db)
    if not one_table:
        raise HTTPException(status_code=404, detail="dominotable.not_found")
    
    str_query = "SELECT dtab.id, dtab.tourney_id, table_number, is_smart, amount_bonus, dtab.image, dtab.is_active, tourney.name " +\
        "FROM events.domino_tables dtab " + \
        "Join events.tourney ON tourney.id = dtab.tourney_id " +\
        " WHERE dtab.id = '" + str(table_id) + "' "  
    lst_data = db.execute(str_query) 
    
    for item in lst_data: 
        result.data = create_dict_row(item, 0, db=db, incluye_tourney=True, api_uri=api_uri)
        
    if not result.data:
        raise HTTPException(status_code=404, detail="event.not_found")
    
    return result

def new(request: Request, profile_id:str, event: EventBase, db: Session, file: File):
    
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    # si el perfil no es de administrador de eventos, no lo puede crear
    
    db_member_profile = get_one_profile(id=profile_id, db=db)
    if not db_member_profile:
        raise HTTPException(status_code=400, detail=_(locale, "userprofile.not_found"))
   
    if db_member_profile.profile_type != 'EVENTADMON':
        raise HTTPException(status_code=400, detail=_(locale, "userprofile.user_not_event_admon"))
    
    one_status = get_one_status_by_name('CREATED', db=db)
    if not one_status:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_found"))
    
    verify_dates(event['start_date'], event['close_date'], locale)
    
    id = str(uuid.uuid4())
    if file:
        ext = get_ext_at_file(file.filename)
        file.filename = str(id) + "." + ext
        
        path = create_dir(entity_type="EVENT", user_id=str(db_member_profile.id), entity_id=str(id))
    
    db_event = Event(id=id, name=event['name'], summary=event['summary'], start_date=event['start_date'], 
                    close_date=event['close_date'], registration_date=event['start_date'], 
                    image=file.filename if file else None, registration_price=float(0.00), 
                    city_id=event['city_id'], main_location=event['main_location'], status_id=one_status.id,
                    created_by=currentUser['username'], updated_by=currentUser['username'], 
                    profile_id=profile_id)
    
    try:
        if file:
            upfile(file=file, path=path)
        
        db.add(db_event)
        db.commit()
        result.data = {'id': id}
        return result
       
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "event.error_new_event")               
        raise HTTPException(status_code=403, detail=msg)

def verify_dates(start_date, close_date, locale):
    
    if start_date > close_date:
        raise HTTPException(status_code=404, detail=_(locale, "dominotable.start_date_incorrect"))
    
    return True

def configure_domino_round(settingtourney: SettingTourneyCreated, db: Session, created_by:str, file=None):
   
    
    # verificar que no exista ese numero de mesa en ese torneo
    str_query = "SELECT count(dtab.id) FROM events.domino_tables dtab " +\
        "where dtab.tourney_id = '" + tourney_id + "' and table_number = " + str(table_number)
        
    amount = db.execute(str_query).fetchone()[0]
    if amount > 0:
        return False
    
    id = str(uuid.uuid4())
    if file:
        ext = get_ext_at_file(file.filename)
        file.filename = str(id) + "." + ext
        
        path = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(id))
        
    
    db_table = DominoTables(id=id, tourney_id=tourney_id, table_number=table_number, is_smart=is_smart,
                            amount_bonus=amount_bonus, is_active=True, created_by=created_by,
                            image=file.filename if file else None,
                            updated_by=created_by, created_date=datetime.now(), updated_date=datetime.now())
        
    try:
        if file:
            upfile(file=file, path=path)
        
        db.add(db_table)
        db.commit()
        return True
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        raise HTTPException(status_code=403, detail='dominotable.error_insert_dominotable')
    
def created_one_domino_round(tourney_id:str, table_number:int, is_smart:bool, amount_bonus:int, db: Session, 
                              created_by:str, file=None):
    
    # verificar que no exista ese numero de mesa en ese torneo
    str_query = "SELECT count(dtab.id) FROM events.domino_tables dtab " +\
        "where dtab.tourney_id = '" + tourney_id + "' and table_number = " + str(table_number)
        
    amount = db.execute(str_query).fetchone()[0]
    if amount > 0:
        return False
    
    id = str(uuid.uuid4())
    if file:
        ext = get_ext_at_file(file.filename)
        file.filename = str(id) + "." + ext
        
        path = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(id))
        
    
    db_table = DominoTables(id=id, tourney_id=tourney_id, table_number=table_number, is_smart=is_smart,
                            amount_bonus=amount_bonus, is_active=True, created_by=created_by,
                            image=file.filename if file else None,
                            updated_by=created_by, created_date=datetime.now(), updated_date=datetime.now())
        
    try:
        if file:
            upfile(file=file, path=path)
        
        db.add(db_table)
        db.commit()
        return True
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        raise HTTPException(status_code=403, detail='dominotable.error_insert_dominotable')
    
def delete(request: Request, table_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    db_table = get_one(table_id, db=db)
    if not db_table:
        raise HTTPException(status_code=404, detail=_(locale, "dominotable.not_found"))
        
    try:
        db_table.is_active = False
        db_table.updated_by = currentUser['username']
        db_table.updated_date = datetime.now()
        db.commit()
            
        if db_table.image:
            
            path = "/public/advertising/"
            try:
                del_image(path=path, name=str(db_table.image))
            except:
                pass
            return result
        else:
            raise HTTPException(status_code=404, detail=_(locale, "dominotable.not_found"))
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "dominotable.imposible_delete"))
    
def update(request: Request, event_id: str, event: EventBase, db: Session, file: File):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
       
    db_event = db.query(Event).filter(Event.id == event_id).first()
    
    if db_event:
        
        if db_event.status_id == 4:  # FINALIZED
            raise HTTPException(status_code=400, detail=_(locale, "event.event_closed"))
    
        if event['name'] and db_event.name != event['name']:
            db_event.name = event['name']
        
        if event['summary'] and db_event.summary != event['summary']:    
            db_event.summary = event['summary']
        
        if file:
            ext = get_ext_at_file(file.filename)
            
            current_image = db_event.image
            file.filename = str(uuid.uuid4()) + "." + ext if ext else str(uuid.uuid4())
            path = create_dir(entity_type="EVENT", user_id=str(currentUser['user_id']), entity_id=str(db_event.id))
            
            user_created = get_one_by_username(db_event.created_by, db=db)
            path_del = "/public/events/" + str(user_created.id) + "/" + str(db_event.id) + "/"
            try:
                del_image(path=path_del, name=str(current_image))
            except:
                pass
            upfile(file=file, path=path)
            db_event.image = file.filename
        
        if event['start_date'] and db_event.start_date != event['start_date']:    
            db_event.start_date = event['start_date']
            
        if event['close_date'] and db_event.close_date != event['close_date']:    
            db_event.close_date = event['close_date']
            
        if event['city_id'] and db_event.city_id != event['city_id']:    
            db_event.city_id = event['city_id']
            
        if event['main_location'] and db_event.main_location != event['main_location']:    
            db_event.main_location = event['main_location']
        
        #desde la interfaz, los que no vengan borrarlos, si vienen nuevos insertarlos, si coinciden modificarlos
        str_tourney_iface = ""
        dict_tourney = {}
        for item in db_event.tourney:
            dict_tourney[item.id] = item
        
        db_event.updated_by = currentUser['username']
        db_event.updated_date = datetime.now()
                
        try:
            db.add(db_event)
            db.commit()
            db.refresh(db_event)
            return result
        except (Exception, SQLAlchemyError) as e:
            print(e.code)
            if e.code == "gkpj":
                raise HTTPException(status_code=400, detail=_(locale, "event.already_exist"))
            
    else:
        pass