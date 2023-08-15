import math
from datetime import datetime

from domino.config.config import settings
from fastapi import HTTPException, Request
from unicodedata import name
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from domino.auth_bearer import decodeJWT
from domino.functions_jwt import get_current_user
from domino.app import _

from domino.models.events.invitations import Invitations
from domino.schemas.events.invitations import InvitationBase, InvitationAccepted
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.resources.utils import get_result_count
from domino.services.events.tourney import get_one as get_tourney_by_id
from domino.services.enterprise.users import get_one_by_username
from domino.services.resources.status import get_one_by_name as get_status_by_name

from domino.services.enterprise.auth import get_url_avatar

def get_one_by_id(invitation_id: str, db: Session):  
    return db.query(Invitations).filter(Invitations.id == invitation_id).first()

def get_all(request:Request, profile_id:str, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
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
    result.data = [create_dict_row(item, page, db=db, incluye_tourney=True, 
                                   host=str(settings.server_uri), port=str(int(settings.server_port))) for item in lst_data]
    
    return result
           
def get_all_invitations_by_tourney(request, tourney_id: str, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    host=str(settings.server_uri)
    port=str(int(settings.server_port))
    
    str_from = "FROM events.invitations " + \
        "inner join enterprise.profile_member ON profile_member.id = invitations.profile_id " + \
        "left join resources.city ON city.id = profile_member.city_id " +\
        "left join resources.country ON country.id = city.country_id " +\
        "WHERE invitations.tourney_id = '" + tourney_id + "' " +\
        " AND status_name = 'ACCEPTED' and profile_member.is_active = True and profile_member.is_ready = True "
        
    str_count = "Select count(*) " + str_from
    str_query = "SELECT invitations.id, invitations.profile_id, profile_member.name, profile_member.photo, " + \
        "city.name as city_name, country.name country_name " + str_from
    
    dict_query = {'name': " AND eve.name ilike '%" + criteria_value + "%'",
                  'summary': " AND summary ilike '%" + criteria_value + "%'",
                  'city_name': " AND city_name ilike '%" + criteria_value + "%'",
                  'start_date': " AND start_date >= '%" + criteria_value + "%'",
                  }
    
    if criteria_key and criteria_key not in dict_query:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    str_count += dict_query[criteria_key] if criteria_value else "" 
    str_query += dict_query[criteria_key] if criteria_value else "" 
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY profile_member.name ASC " 
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(str_query)
    result.data = [create_dict_row_for_tourney(item, host=host, port=port) for item in lst_data]
    
    return result

def create_dict_row_for_tourney(item, host="", port=""):
    
    new_row = {'id': item.id, 'profile_id': item.profile_id, 
               'country': item.country_name, 'city_name': item.city_name,
               'name': item['name'], 
               'photo' : get_url_avatar(item.profile_id, item.photo, host=host, port=port)}
    
    return new_row

def get_all_invitations_by_user(request, profile_id: str, status_name:str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    host=str(settings.server_uri)
    port=str(int(settings.server_port))
                                            
    str_query = "SELECT invitations.id, tourney.name as tourney_name, tourney.modality, tourney.start_date, " + \
        "events.name as event_name, events.close_date, events.main_location, city.name as city_name, " + \
        "country.name country_name, events.id as event_id, events.image, events.profile_id " +\
        "FROM events.invitations " + \
        "inner join events.tourney ON tourney.id = invitations.tourney_id " + \
        "inner join events.events ON events.id = tourney.event_id " + \
        "left join resources.city ON city.id = events.city_id " +\
        "left join resources.country ON country.id = city.country_id " +\
        "WHERE events.invitations.profile_id = '" + profile_id + "' "

    if status_name != 'ALL':
        str_query += " AND invitations.status_name = '" + status_name + "' "
        
    str_query += "ORDER BY tourney.start_date ASC "
    lst_inv = db.execute(str_query)
    result.data = [create_dict_row_invitation(item, host=host, port=port) for item in lst_inv]
    
    return result
 
def create_dict_row_invitation(item, host="", port=""):
    
    image = "http://" + host + ":" + port + "/api/image/" + str(item['profile_id']) + "/" + item['event_id'] + "/" + item['image']
    
    new_row = {'id': item['id'], 'event_name': item['event_name'], 
               'country': item['country_name'], 'city_name': item['city_name'],
               'campus': item['main_location'], 
               'tourney_name': item['tourney_name'], 
               'modality': item['modality'], 
               'startDate': item['start_date'], 'endDate': item['close_date'], 
               'photo' : image}
    
    return new_row
           
def generate_all_user(request, db: Session, tourney_id: str):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    db_tourney = get_tourney_by_id(tourney_id=tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_exist"))
    
    db_status = get_status_by_name('SEND', db=db)
    if not db_status:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_exist"))
    
    dict_modality = {'Individual': "'SINGLE_PLAYER', 'REFEREE'",
                     'Parejas': "'PAIR_PLAYER', 'REFEREE'",
                     'Equipo': "'TEAM_PLAYER', 'REFEREE'"}
    str_profile = dict_modality[db_tourney.modality]
        
    str_users = "SELECT profile_member.id profile_id, eve.name as rolevent_name  " + \
        "FROM enterprise.profile_member " +\
        "inner join enterprise.profile_users ON profile_users.profile_id = profile_member.id and profile_users.is_principal is True " +\
        "inner join enterprise.profile_type eve ON eve.name = profile_member.profile_type " +\
        "where profile_member.is_active=True and profile_member.is_ready=True and eve.name IN (" + str_profile + ") " +\
        "and profile_member.id NOT IN (Select profile_id FROM events.invitations where tourney_id = '" + tourney_id + "') "

    lst_data = db.execute(str_users)
    try:
        for item in lst_data:
            one_invitation = Invitations(tourney_id=db_tourney.id, profile_id=item.profile_id, 
                                         modality=db_tourney.modality,
                                         status_name=db_status.name, created_by=currentUser['username'], 
                                         updated_by=currentUser['username'])
            db.add(one_invitation)
            db.commit()
        
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        # print(e)
        # print(e.__dict__)
        # msg = _(locale, "invitation.error_generate_new")
        # if e.code == 'gkpj':
            # msg = msg + _(locale, "invitation.already_exist")
        
        raise HTTPException(status_code=403, detail=e)
    
def update(request: Request, invitation_id: str, invitation: InvitationAccepted, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
       
    db_invitation = get_one_by_id(invitation_id, db=db)
    if not db_invitation:
        raise HTTPException(status_code=400, detail=_(locale, "invitation.not_exist"))
    
    if db_invitation.status_name == 'SEND':
        status_name = 'ACCEPTED' if invitation.accept else 'REJECTED'
    else:
        status_name = db_invitation.status_name if invitation.accept else 'SEND'
            
    db_status = get_status_by_name(status_name, db=db)
    if not db_status:
        raise HTTPException(status_code=400, detail=_(locale, "status.not_exist"))
    
    db_invitation.status_name = db_status.name
    db_invitation.updated_by = currentUser['username']
    db_invitation.updated_date = datetime.now()
        
    try:
        db.add(db_invitation)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail=_(locale, "invitation.already_exist"))
            
    