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

from domino.models.events.tourney import Players
from domino.schemas.events.player import PlayerBase
from domino.schemas.resources.result_object import ResultObject

from domino.services.resources.status import get_one_by_name, get_one as get_one_status
from domino.services.events.invitations import get_one_by_id as get_invitation_by_id
from domino.services.enterprise.users import get_one_by_username

from domino.services.resources.utils import get_result_count
from domino.services.enterprise.auth import get_url_avatar

def new(request: Request, invitation_id: str, db: Session):
    
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    one_invitation = get_invitation_by_id(invitation_id=invitation_id, db=db)
    if not one_invitation:
        raise HTTPException(status_code=404, detail=_(locale, "invitation.not_found"))
    
    if one_invitation.status_name != 'ACCEPTED':
        raise HTTPException(status_code=404, detail=_(locale, "invitation.status_incorrect"))
    
    one_player = get_one_by_invitation_id(invitation_id, db=db)
    if one_player:
        raise HTTPException(status_code=404, detail=_(locale, "players.already_exist"))
    
    one_player = Players(id=str(uuid.uuid4()), tourney_id=one_invitation.tourney_id, 
                         profile_id=one_invitation.profile_id, nivel='NORMAL', invitation_id=one_invitation.id,
                         created_by=currentUser['username'], updated_by=currentUser['username'], is_active=True)
    try:
        db.add(one_player)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        return False
    
def remove_player(request: Request, player_id: str, db: Session):
    
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    try:
        db_player = db.query(Players).filter(Players.id == player_id).first()
        if db_player:
            db_player.is_active = False
            
            db_player.updated_by = currentUser['username']
            db_player.updated_date = datetime.now()
            
            db.commit()
        else:
            raise HTTPException(status_code=404, detail=_(locale, "player.not_found"))
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail="No es posible eliminar")
    return result
    
def get_all_players_by_tourney(request:Request, page: int, per_page: int, tourney_id: str, is_active: bool, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    str_from = "FROM events.players " +\
        "inner join enterprise.profile_member pro ON pro.id = players.profile_id " +\
        "inner join enterprise.profile_type prot ON prot.name = pro.profile_type " +\
        "left join resources.city ON city.id = pro.city_id " + \
        "left join resources.country ON country.id = city.country_id "
        
    str_count = "Select count(*) " + str_from
    str_query = "SELECT players.id, pro.name as name, prot.description as profile_type, pro.photo, " +\
        "city.name as city_name, country.name as country_name " + str_from
    
    str_where = "WHERE pro.is_ready is True and players.is_active is " + str(is_active) 
    str_where += " AND players.tourney_id = '" + tourney_id + "' " 
    
    str_count += str_where
    str_query += str_where

    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY players.updated_date DESC " 
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, page, db=db, host=str(settings.server_uri), 
                                   port=str(int(settings.server_port))) for item in lst_data]
    
    return result

def create_dict_row(item, page, db: Session, host="", port=""):
    
    # image = ''  #"http://" + host + ":" + port + "/api/image/" + str(item['user_id']) + "/" + item['id'] + "/" + item['image']
    image = get_url_avatar(item['id'], item['photo'], host=host, port=port)
    
    new_row = {'id': item['id'], 'name': item['name'], 
               'profile_type': item['profile_type'],  
               'country': item['country_name'], 'city_name': item['city_name'],  
               'photo' : image}
    if page != 0:
        new_row['selected'] = False
    
    return new_row

def get_one_by_invitation_id(invitation_id: str, db: Session):  
    return db.query(Players).filter(Players.invitation_id == invitation_id).first()