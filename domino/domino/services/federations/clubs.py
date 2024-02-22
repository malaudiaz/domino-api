import math

from fastapi import HTTPException, Request
from unicodedata import name
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from domino.auth_bearer import decodeJWT
from domino.functions_jwt import get_current_user
from domino.app import _

from domino.models.federations.clubs import Federations, Clubs

from domino.schemas.federations.federations import ClubsBase
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.resources.utils import get_result_count
from domino.services.resources.city import get_one as get_one_city
from domino.services.resources.country import get_one as get_one_country
from domino.services.federations.federations import get_one as get_one_federation
            
def get_all(request:Request, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_from = " FROM federations.clubs club LEFT JOIN resources.city ON city.id = club.city_id " +\
        "LEFT JOIN resources.country ON country.id = club.country_id Where club.is_active = True " 
        
    str_count = "Select count(*)" +  str_from
    str_query = "Select club.id, club.name, logo, club.city_id, city.name as city_name, club.country_id, " +\
        "country.name as country_name " + str_from
    
    dict_query = {'name': " WHERE club.name ilike '%" + criteria_value + "%'",
                  'country_id': " WHERE club.country_id =" + criteria_value}
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
        
    str_count += dict_query[criteria_key] if criteria_value else "" 
    str_query += dict_query[criteria_key] if criteria_value else "" 
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY name "
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item) for item in lst_data]
            
    return result

def get_all_by_federation(request:Request, federation_id: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    str_query = "Select club.id, club.name FROM federations.clubs club Where club.is_active = True " +\
        "And federation_id = " + str(federation_id)
    
    lst_data = db.execute(str_query)
    result.data = []
    for item in lst_data:
        result.data.append({'id': item.id, 'name': item.name})
            
    return result

def create_dict_row(item):
    
    new_row = {'id': item['id'], 'name' : item['name'], 'logo' : item['logo'],
               'city_name': item['city_name'], 'country_name': item['country_name']}
    return new_row

def get_one(club_id: str, db: Session):  
    return db.query(Clubs).filter(Clubs.id == club_id).first()

def get_one_by_name(name: str, db: Session):  
    return db.query(Clubs).filter(Clubs.name == name).first()

def get_one_by_id(request, club_id: str, db: Session): 
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    result = ResultObject() 
    result.data = db.query(Clubs).filter(Clubs.id == club_id).first()
    if not result.data:
        raise HTTPException(status_code=404, detail=_(locale, "club.not_found"))
    
    return result
      
def new(request, db: Session, club: ClubsBase):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    db_one_club = get_one_by_name(club.name, db=db)  
    if db_one_club:
        return result
    
    one_federation = get_one_federation(club.federations_id, db=db)
    if not one_federation:
        raise HTTPException(status_code=404, detail=_(locale, "federation.not_found"))
        
    country_id, city_id = None, None
    
    if club.city:
        one_ciy = get_one_city(club.city, db=db)
        if not one_ciy:
            raise HTTPException(status_code=404, detail=_(locale, "city.not_found"))
        else:
            country_id = one_ciy.country_id
            city_id = one_ciy.id
            
    if not country_id and club.country:
        one_country = get_one_country(club.country, db=db)
        if not one_country:
            raise HTTPException(status_code=404, detail=_(locale, "country.not_found"))
        else:
            country_id = one_country.id
    
    db_one_club = Clubs(name=club.name, federation_id=one_federation.id, logo=club.logo, 
                        city_id=city_id, country_id=country_id, is_active=True)
    
    try:
        db.add(db_one_club)
        db.commit()
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "status.error_new_status")
        if e.code == 'gkpj':
            field_name = str(e.__dict__['orig']).split('"')[1].split('_')[1]
            if field_name == 'username':
                msg = msg + _(locale, "status.already_exist")
        
        raise HTTPException(status_code=403, detail=msg)
 
def update(request: Request, club_id: str, club: ClubsBase, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    db_one_club = get_one(club_id, db=db)  
    if db_one_club:
        raise HTTPException(status_code=404, detail=_(locale, "club.not_found"))
    
    if club.city:
        one_ciy = get_one_city(club.city, db=db)
        if not one_ciy:
            raise HTTPException(status_code=404, detail=_(locale, "city.not_found"))
        else:
            db_one_club.country_id = one_ciy.country_id
            db_one_club.city_id = one_ciy.id
            
    if club.country:
        one_country = get_one_country(club.country, db=db)
        if not one_country:
            raise HTTPException(status_code=404, detail=_(locale, "country.not_found"))
        else:
            db_one_club.country_id = one_country.id
            
    db_one_club.name = club.name
    # tema logo
        
    try:
        
        db.add(db_one_club)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail=_(locale, "federation.already_exist"))
   

def delete(request: Request, club_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    db_one_club = get_one(club_id, db=db)  
    if db_one_club:
        raise HTTPException(status_code=404, detail=_(locale, "club.not_found"))
    
    try:
        db_one_club.is_active = False
        db.add(db_one_club)
        db.commit()
        return result
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "club.imposible_delete"))