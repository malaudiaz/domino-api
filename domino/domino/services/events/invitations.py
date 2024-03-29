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

from domino.models.resources.status import StatusElement
from domino.models.events.invitations import Invitations
from domino.models.events.tourney import Tourney

from domino.schemas.events.invitations import InvitationAccepted, InvitationFilters
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.resources.utils import get_result_count
from domino.services.events.tourney import get_one as get_tourney_by_id
from domino.services.enterprise.users import get_one_by_username
from domino.services.resources.status import get_one_by_name as get_status_by_name
from domino.services.resources.country import get_one_by_name as get_country_by_name
from domino.services.enterprise.userprofile import get_type_level

from domino.services.enterprise.auth import get_url_avatar

def get_one_by_id(invitation_id: str, db: Session):  
    return db.query(Invitations).filter(Invitations.id == invitation_id).first()

def get_all(request:Request, profile_id:str, page: int, per_page: int, criteria_key: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    api_uri = str(settings.api_uri)
    
    str_from = "FROM events.tourney tou " +\
        "JOIN resources.entities_status sta ON sta.id = tou.status_id " +\
        "JOIN resources.city city ON city.id = tou.city_id " +\
        "JOIN resources.country country ON country.id = city.country_id " 
        
    str_count = "Select count(*) " + str_from
    str_query = "Select tou.id, tou.name, start_date, inscription_import, city.name as city_name, " +\
        "main_location, summary, image, tou.status_id, sta.name as status_name, country.id as country_id, city.id  as city_id, " +\
        "tou.profile_id as profile_id " + str_from
    
    str_where = " WHERE sta.name != 'CANCELLED' "  
    
    if profile_id:
        str_where += "AND profile_id = '" + profile_id + "' "
    # debo incluir los de los perfiles que el sigue
    
    dict_query = {'name': " AND tou.name ilike '%" + criteria_value + "%'",
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
    result.data = [create_dict_row_invitation(item, page, db=db, incluye_tourney=True, api_uri=api_uri) for item in lst_data]
    
    return result
           
def get_all_invitations_by_tourney(request, tourney_id: str, page: int, per_page: int, criteria_key: str, criteria_value: str, 
                                   player_name:str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    api_uri = str(settings.api_uri)
    
    db_tourney = get_tourney_by_id(tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
   
    # Me pasan status_id para filtrar por este parametro: 0: Enviadas, 1: Aceptadas, 2: Rechazadas
    str_status = ''
    if criteria_key and criteria_key == 'status_id':
        # str_status = '' if criteria_value == '0' else " AND (status_name = 'ACCEPTED' or status_name = 'CONFIRMED') " \
        #     if criteria_value == '1' else " AND status_name = 'REFUTED' "  
        # en las aceptadas no devolver los confirmados..
        
        str_status = " AND status_name = 'SEND' " if criteria_value == '0' else " AND status_name = 'ACCEPTED' " \
            if criteria_value == '1' else " AND status_name = 'REFUTED' " # if criteria_value == '2' else " AND status_name = 'SEND' " 
    
    str_from = "FROM events.invitations " + \
        "inner join enterprise.profile_member ON profile_member.id = invitations.profile_id " + \
        "left join resources.city ON city.id = profile_member.city_id " +\
        "left join resources.country ON country.id = city.country_id " +\
        "JOIN resources.entities_status sta ON sta.name = invitations.status_name "
        
    dict_modality = {'Individual': "join enterprise.profile_single_player player ON player.profile_id = profile_member.id " +\
                     "JOIN federations.clubs club ON club.id = player.club_id ",
                     'Parejas': "join enterprise.profile_pair_player player ON player.profile_id = profile_member.id ",
                     'Equipo': "join enterprise.profile_team_player player ON player.profile_id = profile_member.id "}
    
    str_from += dict_modality[db_tourney.modality]
    str_from += "WHERE invitations.tourney_id = '" + tourney_id + "' " +\
        "and profile_member.is_active = True and profile_member.is_ready = True "
        
    str_from += str_status
    
    if player_name:    
        str_from += " AND profile_member.name ilike '%" + player_name + "%'"
        
    str_count = "Select count(*) " + str_from
    str_query = "SELECT invitations.id, invitations.profile_id, profile_member.name, profile_member.photo, " + \
        "city.name as city_name, country.name country_name, player.level, player.elo, " +\
        "sta.id as status_id, sta.name as status_name, sta.description as status_description "
    if db_tourney.modality == 'Individual':
        str_query += ", club.siglas as club_siglas "
        
    str_query += str_from
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY player.elo DESC, profile_member.name ASC " 
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(str_query)
    result.data = [create_dict_row_for_tourney(item, api_uri=api_uri, modality=db_tourney.modality) for item in lst_data]
    
    return result

def create_dict_row_for_tourney(item, api_uri="", modality=''):
    
    club_siglas = item.club_siglas if modality and modality == 'Individual' else ''
    level_name = get_type_level(item['level']) if item.level else '' 
    new_row = {'id': item.id, 'profile_id': item.profile_id, 
               'country': item.country_name if item.country_name else '', 'city_name': item.city_name if item.city_name else '',
               'name': item['name'], 'status_id': item['status_id'], 
               'elo': item['elo'], 'level': level_name, 'club_siglas': club_siglas,
               'status_name': item['status_name'], 'status_description': item['status_description'],
               'photo' : get_url_avatar(item.profile_id, item.photo, api_uri=api_uri)}
    
    return new_row

def get_all_invitations_by_user(request, profile_id: str, status_name:str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    api_uri = str(settings.api_uri)
                                            
    str_query = "SELECT invitations.id, tourney.name as tourney_name, tourney.modality, tourney.start_date, " + \
        "city.name as city_name, country.name country_name, tourney.image, tourney.profile_id " +\
        "FROM events.invitations " + \
        "inner join events.tourney ON tourney.id = invitations.tourney_id " + \
        "left join resources.city ON city.id = tourney.city_id " +\
        "left join resources.country ON country.id = city.country_id " +\
        "WHERE events.invitations.profile_id = '" + profile_id + "' "

    if status_name != 'ALL':
        str_query += " AND invitations.status_name = '" + status_name + "' "
        
    str_query += "ORDER BY tourney.start_date ASC "
    lst_inv = db.execute(str_query)
    result.data = [create_dict_row_invitation(item, api_uri=api_uri) for item in lst_inv]
    
    return result
 
def create_dict_row_invitation(item, api_uri=""):
    
    image = api_uri + "/api/image/" + str(item['profile_id']) + "/" + item['event_id'] + "/" + item['image']
    
    new_row = {'id': item['id'], 'country': item['country_name'], 'city_name': item['city_name'],
               'campus': item['main_location'], 'tourney_name': item['tourney_name'], 
               'modality': item['modality'], 'startDate': item['start_date'], 'endDate': item['close_date'], 
               'photo' : image}
    
    return new_row
           
def generate_all_user(request, db: Session, tourney_id: str, filters_invitation: InvitationFilters):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    db_tourney = get_tourney_by_id(tourney_id=tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_exist"))
    
    one_status = get_status_by_name('CREATED', db=db)
    if not one_status:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_exist"))
    
    if db_tourney.status_id != one_status.id:
        raise HTTPException(status_code=404, detail=_(locale, "status.incorrect"))
    
    db_status_send = get_status_by_name('SEND', db=db)
    if not db_status_send:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_exist"))
    
    result = generate_for_tourney(db_tourney, db_status_send, currentUser['username'], filters_invitation, db=db)
    
    return result
    
def generate_for_tourney(db_tourney:Tourney, db_status: StatusElement, username: str, filters_invitation: InvitationFilters, db: Session):
    
    dict_modality = {'Individual': "'SINGLE_PLAYER', 'REFEREE'",
                     'Parejas': "'PAIR_PLAYER', 'REFEREE'",
                     'Equipo': "'TEAM_PLAYER', 'REFEREE'"}
    str_profile = dict_modality[db_tourney.modality]
    
    str_join_country = "left join resources.city ON city.id = enterprise.profile_member.city_id " +\
        "left join resources.country ON country.id = city.country_id "
        
    dict_modality_join = {'Individual': "join enterprise.profile_single_player player ON player.profile_id = profile_member.id ",
                          'Parejas': "join enterprise.profile_pair_player player ON player.profile_id = profile_member.id ",
                          'Equipo': "join enterprise.profile_team_player player ON player.profile_id = profile_member.id "}
    
    str_join_elo = dict_modality_join[db_tourney.modality]
            
    str_where = "where profile_member.is_active=True and profile_member.is_ready=True and eve.name IN (" + str_profile + ") " +\
        "and profile_member.id NOT IN (Select profile_id FROM events.invitations where tourney_id = '" + db_tourney.id + "') "
        
    str_users = "SELECT profile_member.id profile_id, eve.name as rolevent_name  " + \
        "FROM enterprise.profile_member " +\
        "inner join enterprise.profile_users ON profile_users.profile_id = profile_member.id and profile_users.is_principal is True " +\
        "inner join enterprise.profile_type eve ON eve.name = profile_member.profile_type "
    
    str_filter = ''
    if filters_invitation:  # viene con filtros
        if filters_invitation.player:
            str_filter += " AND enterprise.profile_member.name ilike '%" + filters_invitation.player + "%'"
        if filters_invitation.country:
            str_users += str_join_country
            country = get_country_by_name(filters_invitation.country, db=db)
            if country:
                str_filter += " AND resources.country.id = " + str(country.id) 
        if filters_invitation.elo_min or filters_invitation.elo_max:
            str_users += str_join_elo
            if filters_invitation.elo_min:
                str_filter += " AND player.elo >= " + str(filters_invitation.elo_min) 
            if filters_invitation.elo_max:
                str_filter += " AND player.elo <= " + str(filters_invitation.elo_max) 
    
    str_users += str_where + str_filter
    lst_data = db.execute(str_users)
    
    try:
        for item in lst_data:
            one_invitation = Invitations(tourney_id=db_tourney.id, profile_id=item.profile_id, 
                                         modality=db_tourney.modality,
                                         status_name=db_status.name, created_by=username, updated_by=username)
            db.add(one_invitation)
        
        db.commit()
        return ResultObject()
     
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        # print(e)
        # print(e.__dict__)
        # msg = _(locale, "invitation.error_generate_new")
        # if e.code == 'gkpj':
            # msg = msg + _(locale, "invitation.already_exist")
        
        raise HTTPException(status_code=403, detail=e)
    
    return True
    
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
            
def get_amount_invitations_by_tourney(tourney_id: str, db: Session):  
    
    str_count = "Select count(*) FROM events.invitations WHERE invitations.tourney_id = '" + tourney_id + "' "
    amount = db.execute(str_count).scalar()
    return amount