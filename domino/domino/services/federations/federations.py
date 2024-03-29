import math
import uuid

from datetime import datetime
from fastapi import HTTPException, Request, UploadFile, File
from unicodedata import name
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from domino.auth_bearer import decodeJWT
from domino.functions_jwt import get_current_user
from domino.config.config import settings
from domino.app import _

from domino.models.federations.clubs import Federations, Clubs

from domino.schemas.federations.federations import FederationsBase
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.resources.utils import get_result_count, create_dir, del_image, get_ext_at_file, upfile
from domino.services.resources.city import get_one as get_one_city, get_list_by_country_id
from domino.services.resources.country import get_one as get_one_country

from domino.services.enterprise.auth import get_url_federation

            
def get_all(request:Request, page: int, per_page: int, profile_id: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    api_uri = api_uri = str(settings.api_uri)
    
    str_from = " FROM federations.federations fed LEFT JOIN resources.city ON city.id = fed.city_id " +\
        "LEFT JOIN resources.country ON country.id = fed.country_id Where fed.is_active = True " +\
        "and fed.id IN (Select federation_id from enterprise.profile_member pm " +\
        "join enterprise.profile_event_admon pa ON pa.profile_id = pm.id " +\
        "where profile_type IN ('EVENTADMON', 'FEDERATED') " +\
        " and id = '" + profile_id + "') "
        
    str_count = "Select count(*)" +  str_from
    str_query = "Select fed.id, fed.name, fed.siglas, logo, fed.city_id, city.name as city_name, fed.country_id, " +\
        "country.name as country_name " + str_from
    
    str_criteria = " AND (fed.name ilike '%" + criteria_value + "%' OR fed.siglas ilike '%" +  criteria_value + "%'" +\
        " OR city.name ilike '%" + criteria_value + "%' OR country.name ilike '%" + criteria_value + "%') " if criteria_value else ''
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
        
    str_count += str_criteria
    str_query += str_criteria
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY name "
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    
    result.data = [create_dict_row(item, api_uri=api_uri) for item in lst_data]
            
    return result

def get_all_list(request:Request, profile_id:str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    str_query = "Select fed.id, fed.name FROM federations.federations fed " +\
        "Where fed.is_active = True " +\
        "and fed.id IN (Select federation_id from enterprise.profile_member pm " +\
        "join enterprise.profile_event_admon pa ON pa.profile_id = pm.id " +\
        "where profile_type IN ('EVENTADMON', 'FEDERATED') " +\
        " and id = '" + profile_id + "') ORDER BY id  "
     
    lst_data = db.execute(str_query)
    result.data = []
    for item in lst_data:
        result.data.append({'id': item.id, 'name': item.name})
            
    return result

def create_dict_row(item, api_uri=''):
    
    api_uri = api_uri = str(settings.api_uri) if not api_uri else api_uri
    
    logo = api_uri + "/api/federations/" + str(item['id']) + "/" + item['logo'] if item['logo'] else None
    
    new_row = {'id': item['id'], 'name' : item['name'], 'logo' : logo, 'siglas' : item['siglas'],
               'city_name': item['city_name'], 'country_name': item['country_name']}
    return new_row

def get_one(federation_id: str, db: Session):  
    return db.query(Federations).filter(Federations.id == federation_id).first()

def get_one_by_id(request, federation_id: str, db: Session): 
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    api_uri = api_uri = str(settings.api_uri)
    
    result = ResultObject() 
    one_federation = get_one(federation_id=federation_id, db=db)
    if not one_federation:
        raise HTTPException(status_code=404, detail=_(locale, "federation.not_found"))
    
    logo = api_uri + "/api/federations/" + str(one_federation.id) + "/" + one_federation.logo if one_federation.logo else ''
    
    result.data = {'id': one_federation.id, 'name' : one_federation.name, 'logo' : logo, 'siglas' : one_federation.siglas,
                   'city_name': one_federation.city.name if one_federation.city else '', 
                   'city_id': one_federation.city.id if one_federation.city else '', 
                   'country_id': one_federation.country.id if one_federation.country else '',
                   'country_name': one_federation.country.name if one_federation.country else ''}
     
    return result

def get_city_at_federation(request, profile_id: str, db: Session): 
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_query = "Select city.id, city.name from enterprise.profile_event_admon pev " +\
        "join federations.federations fed ON fed.id = pev.federation_id " +\
        "join resources.country country ON country.id = fed.country_id " +\
        "JOIN resources.city city ON city.country_id = country.id " +\
        "where fed.is_active = True and pev.profile_id = '" + profile_id + "' order by name " 

    result = ResultObject() 
    lst_data = db.execute(str_query)
    
    result.data = []
    for item in lst_data:
        result.data.append({'id': item.id, 'name': item.name})
    return result
    
def get_one_by_name(name: str, db: Session):  
    return db.query(Federations).filter(Federations.name == name).first()

def get_one_by_siglas(siglas: str, db: Session):  
    return db.query(Federations).filter(Federations.siglas == siglas).first()
      
def new(request, federation: FederationsBase, logo: File, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
   
    result = ResultObject() 
    
    db_one_federation = get_one_by_siglas(federation['siglas'], db=db)  
    if db_one_federation:
        raise HTTPException(status_code=404, detail=_(locale, "federation.siglas_exist"))
    
    country_id, city_id = None, None
    
    if federation['city']:
        one_ciy = get_one_city(federation['city'], db=db)
        if not one_ciy:
            raise HTTPException(status_code=404, detail=_(locale, "city.not_found"))
        else:
            country_id = one_ciy.country_id
            city_id = one_ciy.id
            
    if not country_id and federation['country']:
        one_country = get_one_country(federation['country'], db=db)
        if not one_country:
            raise HTTPException(status_code=404, detail=_(locale, "country.not_found"))
        else:
            country_id = one_country.id
    
    logo_name = ''
    if logo:
        logo_id = str(uuid.uuid4())
        ext = get_ext_at_file(logo.filename)
        logo.filename = logo_id + "." + ext
        logo_name = logo.filename
        
    db_one_federation = Federations(name=federation['name'], siglas=federation['siglas'], logo=logo_name,
                                    city_id=city_id, country_id=country_id, is_active=True)
    
    try:
        db.add(db_one_federation)
        db.commit()
        db.refresh(db_one_federation)
        
        if logo_name:
            path_federation = create_dir(entity_type='FEDERATION', user_id=None, entity_id=str(db_one_federation.id))
            upfile(file=logo, path=path_federation)
        
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "status.error_new_status")
        if e.code == 'gkpj':
            field_name = str(e.__dict__['orig']).split('"')[1].split('_')[1]
            if field_name == 'username':
                msg = msg + _(locale, "status.already_exist")
        
        raise HTTPException(status_code=403, detail=msg)

def update(request: Request, federation_id: str, federation: FederationsBase, logo: File, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    result = ResultObject() 
    
    db_one_federation = get_one(federation_id, db=db)  
    if not db_one_federation:
        raise HTTPException(status_code=404, detail=_(locale, "federation.not_found"))
    
    if federation['city'] and federation['city'] != db_one_federation.city_id:
        one_ciy = get_one_city(federation['city'], db=db)
        if not one_ciy:
            raise HTTPException(status_code=404, detail=_(locale, "city.not_found"))
        else:
            db_one_federation.country_id = one_ciy.country_id
            db_one_federation.city_id = one_ciy.id
            
    if federation['country']:
        one_country = get_one_country(federation['country'], db=db)
        if not one_country:
            raise HTTPException(status_code=404, detail=_(locale, "country.not_found"))
        else:
            db_one_federation.country_id = one_country.id
    
    # siglas no se pueden repetir
    if federation['siglas'] and federation['siglas'] != db_one_federation.siglas:  
        one_federation_by_siglas = get_one_by_siglas(federation['siglas'], db=db)
        if one_federation_by_siglas:
            raise HTTPException(status_code=404, detail=_(locale, "federation.siglas_exist"))
        db_one_federation.siglas = federation['siglas']
        
    if federation['name'] and federation['name'] != db_one_federation.name:      
        db_one_federation.name = federation['name']
        
    logo_name = ''
    if logo:
        if db_one_federation.logo:  # borrar la actual
            current_image = db_one_federation.logo
            path_del = "/public/federations/" + str(db_one_federation.id) + "/"
            try:
                del_image(path=path_del, name=str(current_image))
            except:
                pass
            
        logo_id = str(uuid.uuid4())
        ext = get_ext_at_file(logo.filename)
        logo.filename = logo_id + "." + ext
        logo_name = logo.filename
        
        db_one_federation.logo = logo_name
           
    # try:
    db.add(db_one_federation)
    db.commit()
    
    if logo_name:
        path_federation = create_dir(entity_type='FEDERATION', user_id=None, entity_id=str(db_one_federation.id))
        upfile(file=logo, path=path_federation)
        
    return result
    # except (Exception, SQLAlchemyError) as e:
    #     print(e.code)
    #     if e.code == "gkpj":
    #         raise HTTPException(status_code=400, detail=_(locale, "federation.already_exist"))
 
def delete(request: Request, federation_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    db_one_federation = get_one(federation_id, db=db)  
    if not db_one_federation:
        raise HTTPException(status_code=404, detail=_(locale, "federation.not_found"))
    
    try:
        db_one_federation.is_active = False
        db.add(db_one_federation)
        db.commit()
        return result
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "federation.imposible_delete"))
    
def save_logo_federation(request: Request, siglas: str, logo: File, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    api_uri = api_uri = str(settings.api_uri)
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    one_federation = get_one_by_siglas(siglas, db=db)
    if not one_federation:
        one_federation = Federations(name='Nueva Creación', siglas=siglas, is_active=True)
         
        # raise HTTPException(status_code=404, detail=_(locale, "federation.not_found"))
    
    path_tourney = create_dir(entity_type='FEDERATION', user_id=None, entity_id=str(one_federation.id))
    
    #puede venir la foto o no venir y eso es para borrarla.
    if one_federation.logo:  # ya tiene una imagen asociada
        current_image = one_federation.logo
        try:
            del_image(path=path_tourney, name=str(current_image))
        except:
            pass
    
    if not logo:
        one_federation.logo = None
    else:  
        str(uuid.uuid4()) 
        ext = get_ext_at_file(logo.filename)
        logo.filename = str(uuid.uuid4()) + "." + ext
        
        upfile(file=logo, path=path_tourney)
        one_federation.logo = logo.filename
    
    try:
        db.add(one_federation)
        db.commit()
        result.data = {'id': one_federation.id, 'url': get_url_federation(one_federation.id, one_federation.logo, api_uri=api_uri)}
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail=_(locale, "event.already_exist"))
