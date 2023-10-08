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

from domino.models.events.domino_tables import DominoTables, FilesTables
from domino.models.events.tourney import SettingTourney

from domino.schemas.events.tourney import TourneyCreated, SettingTourneyCreated
from domino.schemas.events.events import EventBase, EventSchema
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.resources.status import get_one_by_name as get_one_status_by_name, get_one as get_one_status
from domino.services.resources.utils import get_result_count, upfile, create_dir, del_image, get_ext_at_file, remove_dir
from domino.services.enterprise.userprofile import get_one as get_one_profile
                         
def get_all(request:Request, profile_id:str, tourney_id:str, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    api_uri = str(settings.api_uri)
    
    # verificar que el perfil sea admon del evento al cual pertenece el torneo.
    db_member_profile = get_one_profile(id=profile_id, db=db)
    if not db_member_profile:
        raise HTTPException(status_code=400, detail=_(locale, "userprofile.not_found"))
   
    if db_member_profile.profile_type != 'EVENTADMON':
        raise HTTPException(status_code=400, detail=_(locale, "userprofile.user_not_event_admon"))
    
    str_from = "FROM events.domino_tables dtab " +\
        "JOIN events.tourney dtou ON dtou.id = dtab.tourney_id " +\
        "JOIN events.setting_tourney stou ON stou.tourney_id = dtou.id "  
        
    str_count = "Select count(*) " + str_from
    str_query = "Select dtab.id, table_number, is_smart, amount_bonus, dtab.image, dtab.is_active, " +\
        "dtou.id as tourney_id, dtou.name, stou.image as image_tourney " + str_from
    
    str_where = " WHERE dtab.tourney_id = '" + tourney_id + "' "  
    
    dict_query = {'table_number': " AND table_number = " + criteria_value}
    
    str_count += str_where
    str_query += str_where
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    str_count += dict_query[criteria_key] if criteria_value else "" 
    str_query += dict_query[criteria_key] if criteria_value else "" 
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY table_number " 
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, tourney_id, page, db=db, api_uri=api_uri) for item in lst_data]
    
    return result

def create_dict_row(item, tourney_id, page, db: Session, api_uri=""):
    
    image_name = item['image'] if item['image'] else item['image_tourney']
    image = api_uri + "/api/public/advertising/" + str(item['tourney_id']) + "/" + image_name
    
    new_row = {'id': item['id'], 'table_number': item['table_number'], 
               'is_smart': item['is_smart'], 'amount_bonus': item['amount_bonus'], 
               'tourney_name': item['name'], 'is_active': item['is_active'],
               'photo' : image, 'filetables':[]}
    if page != 0:
        new_row['selected'] = False
        
    if item['is_smart']:
        str_files = "Select id, position, is_ready from events.files_tables Where table_id = '" + item['id'] + "' "
        lst_files = db.execute(str_files)
        for item_f in lst_files:
            new_row['filetables'].append({'file_id': item_f.id, 'position': item_f.position, 'is_ready': item_f.is_ready})
    
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
        result.data = [create_dict_row(item, one_table.tourney_id, 0, db=db, api_uri=api_uri) for item in lst_data]
        
    if not result.data:
        raise HTTPException(status_code=404, detail="dominotable.not_found")
    
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

def configure_domino_tables(db_tourney, settingtourney: SettingTourney, db: Session, created_by:str, file=None):
    
    bonus = settingtourney.amount_bonus_points // settingtourney.amount_bonus_tables
    table_number = 0
    amount_trad_tables = settingtourney.amount_tables - settingtourney.amount_smart_tables
   
    # crear las mesas inteligentes
    if settingtourney.amount_smart_tables > 0:
        for i in range(settingtourney.amount_smart_tables):
            table_number += 1
            created_one_domino_tables(db_tourney, table_number, True, bonus, db, created_by)
            bonus -= 1
    
    # crear las mesas tradicionales
    for i in range(amount_trad_tables):
        table_number += 1
        created_one_domino_tables(db_tourney, table_number, False, bonus, db, created_by)
        bonus -= 1
        
    return True
   
def created_one_domino_tables(db_tourney, table_number:int, is_smart:bool, amount_bonus:int, db: Session, 
                              created_by:str, file=None):
    
    # verificar que no exista ese numero de mesa en ese torneo
    str_query = "SELECT count(dtab.id) FROM events.domino_tables dtab " +\
        "where dtab.tourney_id = '" + db_tourney.id + "' and table_number = " + str(table_number)
        
    amount = db.execute(str_query).fetchone()[0]
    if amount > 0:
        return False
    
    id = str(uuid.uuid4())
    if file:
        ext = get_ext_at_file(file.filename)
        file.filename = str(id) + "." + ext
        
        path = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(id))
        
    db_table = DominoTables(id=id, tourney_id=db_tourney.id, table_number=table_number, is_smart=is_smart,
                            amount_bonus=amount_bonus if amount_bonus >= 0 else 0, is_active=True, created_by=created_by,
                            image=file.filename if file else None,
                            updated_by=created_by, created_date=datetime.now(), updated_date=datetime.now())
    
    if is_smart:
        for i in range(4):
            i += 1
            file_id = str(uuid.uuid4())
            db_files = FilesTables(id=file_id, position=i, is_ready=False)
            db_table.filestable.append(db_files)
        
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
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "dominotable.imposible_delete"))
    
    return result

# por ahora solo modifica imagen y bonus...   
def update(request: Request, id: str, amount_bonus: int, db: Session, file: File):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    # verificar si la ronda esta en el estado en que se puede cambiar la mesa (CREADA) 
      
    db_table = get_one(id, db=db)
    if not db_table:
        raise HTTPException(status_code=404, detail=_(locale, "dominotable.not_found"))
    
    db_table.amount_bonus = amount_bonus
    
    if file:
        ext = get_ext_at_file(file.filename)
        file.filename = str(id) + "." + ext
        
    if file:
        ext = get_ext_at_file(file.filename)
        
        if db_table.image:  # ya tiene una imagen asociada
            current_image = db_table.image
        
        file.filename = str(id) + "." + ext
        path = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(id))
        
        path_del = "/public/advertising/" + str(db_table.id) + "/"
        try:
            del_image(path=path_del, name=str(current_image))
        except:
            pass
        
        upfile(file=file, path=path)
        db_table.image = file.filename
    
    db_table.updated_by = currentUser['username']
    db_table.updated_date = datetime.now()
            
    try:
        db.add(db_table)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail=_(locale, "event.already_exist"))
