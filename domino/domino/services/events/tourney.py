import math
import uuid
from typing import List
from datetime import datetime
from fastapi import HTTPException, Request, File
from unicodedata import name
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from domino.auth_bearer import decodeJWT
from domino.functions_jwt import get_current_user
from domino.app import _
from domino.config.config import settings

from domino.models.events.tourney import Tourney, DominoCategory

from domino.schemas.events.tourney import TourneyCreated, SettingTourneyCreated, DominoCategoryCreated
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.resources.status import get_one_by_name as get_one_status_by_name, get_one as get_one_status

from domino.services.resources.utils import get_result_count
from domino.services.events.domino_table import created_one_domino_tables

from domino.services.resources.utils import get_result_count, upfile, create_dir, del_image, get_ext_at_file, remove_dir, copy_image, del_image
from domino.services.enterprise.userprofile import get_one as get_one_profile

from domino.services.enterprise.auth import get_url_advertising, get_url_avatar
from domino.services.events.calculation_serv import format_number
            
def get_all(request:Request, page: int, per_page: int, profile_id: str, criteria_value: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    api_uri = str(settings.api_uri)
    
    str_from = "FROM events.tourney tou " +\
        "JOIN resources.entities_status sta ON sta.id = tou.status_id " +\
        "JOIN federations.federations fed ON fed.id = tou.federation_id " +\
        "LEFT JOIN resources.city city ON city.id = tou.city_id " +\
        "LEFT JOIN resources.country country ON country.id = city.country_id " 
    
    str_count = "Select count(*) " + str_from
    str_query = "Select tou.id, tou.modality, tou.name, tou.summary, tou.start_date, " +\
        "city.id  as city_id, city.name as city_name, inscription_import, amount_rounds, main_location, " +\
        "tou.status_id, sta.name as status_name, sta.description as status_description, tou.image " + str_from
    
    str_where = " WHERE sta.name != 'CANCELLED' "  
    
    if profile_id:
        str_where += "AND profile_id = '" + profile_id + "' "
        
    str_where += " AND (tou.name ilike '%" + criteria_value + "%' OR tou.modality ilike '%" +  criteria_value + "%'" +\
        " OR tou.summary ilike '%" + criteria_value + "%'  OR city.name ilike '%" + criteria_value + \
        "%' OR main_location ilike '%" + criteria_value + "%') " if criteria_value else ''
    
    str_count += str_where
    str_query += str_where
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY start_date " 
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
     
    lst_data = db.execute(str_query)
    
    result.data = [create_dict_row(item, api_uri=api_uri) for item in lst_data]
    
    return result

def create_dict_row(item, api_uri:str):
    
    new_row = {'id': item['id'], 'name': item['name'], 'modality': item['modality'], 'summary' : item['summary'], 
               'startDate': item['start_date'], 'main_location': item['main_location'] if item['main_location'] else '',
               'city_id': item['city_id'] if item['city_id'] else '', 'city_name': item['city_name'] if item['city_name'] else '',
               'status_id': item['status_id'], 'status_name': item['status_name'], 'status_description': item['status_description'],
               'number_rounds': item['amount_rounds'], 'inscription_import': item['inscription_import'] if item['inscription_import'] else 0.00,
               'image': get_url_advertising(tourney_id=item['id'], file_name=item['image'] if item['image'] else None, api_uri=api_uri)
               }
       
    return new_row

def get_one(tourney_id: str, db: Session):  
    return db.query(Tourney).filter(Tourney.id == tourney_id).first()

def get_one_by_name(tourney_name: str, db: Session):  
    return db.query(Tourney).filter(Tourney.name == tourney_name).first()

def get_one_by_id(tourney_id: str, db: Session): 
    result = ResultObject()  
    
    api_uri = str(settings.api_uri)
    
    str_query = "Select tou.id, tou.modality, tou.name, tou.summary, tou.start_date, " +\
        "amount_rounds, tou.image, tou.main_location, tou.inscription_import, " +\
        "city.id  as city_id, city.name as city_name, " +\
        "tou.status_id, sta.name as status_name, sta.description as status_description FROM events.tourney tou " +\
        "JOIN federations.federations fed ON fed.id = tou.federation_id " +\
        "JOIN resources.entities_status sta ON sta.id = tou.status_id " +\
        "LEFT JOIN resources.city city ON city.id = tou.city_id " +\
        " WHERE tou.id = '" + str(tourney_id)  + "' "
    
    lst_data = db.execute(str_query)
    if lst_data:
        for item in lst_data:
            result.data = create_dict_row(item, api_uri=api_uri)
            
    return result

def get_count_players_by_tourney(tourney_id: str, db: Session):  
    
    str_query = "Select count(*) FROM events.players " +\
        "JOIN resources.entities_status sta ON sta.id = events.players.status_id " +\
        "WHERE players.tourney_id = '" + tourney_id + "' AND sta.name != 'CANCELLED'" 
    
    amount_player = db.execute(str_query).scalar()
    
    return amount_player

def get_all_by_event_id(event_id: str, db: Session): 
    result = ResultObject() 
    
    api_uri = str(settings.api_uri) 
    
    str_from = "FROM events.tourney tou " +\
        "JOIN events.events eve ON eve.id = tou.event_id " +\
        "JOIN resources.entities_status sta ON sta.id = tou.status_id "
    
    str_query = "Select tou.id, event_id, eve.name as event_name, tou.modality, tou.name, tou.summary, tou.start_date, " +\
        "tou.status_id, sta.name as status_name, lottery_type, number_rounds, tou.image " + str_from
    
    str_query += " WHERE sta.name != 'CANCELLED' and event_id = '" + str(event_id) + "' ORDER BY start_date "  
    lst_data = db.execute(str_query)
    result.data = [create_dict_row(item, 0, api_uri, db=db) for item in lst_data]
    
    return result

def new(request, profile_id: str, tourney: TourneyCreated, image: File, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    one_profile = get_one_profile(profile_id, db=db)
    if not one_profile:
        raise HTTPException(status_code=404, detail=_(locale, "userprofile.not_found"))
    
    if one_profile.profile_type != "EVENTADMON":
        raise HTTPException(status_code=404, detail=_(locale, "userprofile.profile_incorrect"))
    
    one_status = get_one_status_by_name('CREATED', db=db)
    if not one_status:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_found"))
    
    id = str(uuid.uuid4())
    K1= get_factor_scale()
    
    db_tourney = Tourney(id=id, modality=tourney['modality'], name=tourney['name'], summary=tourney['summary'], 
                         start_date=tourney['startDate'], status_id=one_status.id, created_by=currentUser['username'], 
                         game_system='SUIZO', amount_rounds=tourney['number_rounds'], updated_by=currentUser['username'], 
                         profile_id=one_profile.id, federation_id=one_profile.profile_event_admon[0].federation_id,
                         constant_increase_elo=K1, main_location=tourney['main_location'], inscription_import=tourney['inscription_import'],
                         city_id=tourney['city_id'])
    db.add(db_tourney)
    
    #crear la carpeta con la imagen de la publicidad....
    path_tourney = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(id))

    image_name = ''
    if image:
        ext = get_ext_at_file(image.filename)
        image.filename = id + "." + ext
        upfile(file=image, path=path_tourney)
        image_name = image.filename
        
    else:
        image_domino="public/smartdomino.png"
        image_destiny = path_tourney + "smartdomino.png"
        copy_image(image_domino, image_destiny)
        image_name = "smartdomino.png"
       
    db_tourney.image = image_name
        
    try:
        
        db.commit()
        return result
       
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "tourney.error_new_tourney")               
        raise HTTPException(status_code=403, detail=msg)

def delete(request: Request, tourney_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    one_status = get_one_status_by_name('CANCELLED', db=db)
    if not one_status:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_found"))
    
    db_tourney= db.query(Tourney).filter(Tourney.id == tourney_id).first()
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
    
    if db_tourney.status.name != 'CREATED':
        raise HTTPException(status_code=404, detail=_(locale, "tourney.status_incorrect"))
    
    try:
        
        path_tourney = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(tourney_id))
        
        if db_tourney.image:  # tiene una imagen asociada
            try:
                del_image(path=path_tourney, name=str(db_tourney.image))
            except:
                pass
                
        db_tourney.status_id = one_status.id
        db_tourney.updated_by = currentUser['username']
        db_tourney.updated_date = datetime.now()
        db.commit()
        return result
        
    except (Exception, SQLAlchemyError) as e:
        print(e)
        raise HTTPException(status_code=404, detail=_(locale, "tourney.imposible_delete"))
    
def update(request: Request, tourney_id: str, tourney: TourneyCreated, image: File, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    one_status_end = get_one_status_by_name('FINALIZED', db=db)
    
    db_tourney = get_one(tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
    
    if db_tourney.status_id == one_status_end.id:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.tourney_closed"))
    
    if tourney['name'] and db_tourney.name != tourney['name']:
        db_tourney.name = tourney['name']
        
    if tourney['summary'] and db_tourney.summary != tourney['summary']:
        db_tourney.summary = tourney['summary']
        
    if tourney['modality'] and db_tourney.modality != tourney['modality']:
        db_tourney.modality = tourney['modality']
        
    if tourney['startDate'] and db_tourney.start_date != tourney['startDate']:
        db_tourney.start_date = tourney['startDate']
        
    if tourney['number_rounds'] and db_tourney.amount_rounds != tourney['number_rounds']:
        db_tourney.amount_rounds = tourney['number_rounds']
        
    if tourney['main_location'] and db_tourney.main_location != tourney['main_location']:
        db_tourney.main_location = tourney['main_location']
        
    if tourney['inscription_import'] and db_tourney.inscription_import != tourney['inscription_import']:
        db_tourney.inscription_import = tourney['inscription_import']
        
    if tourney['city_id'] and db_tourney.city_id != tourney['city_id']:
        db_tourney.city_id = tourney['city_id']
        
    db_tourney.updated_by = currentUser['username']
    db_tourney.updated_date = datetime.now()
    
    path_tourney = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(db_tourney.id))
    
    if image:
        if db_tourney.image:  # ya tiene una imagen asociada
            current_image = db_tourney.image
            try:
                del_image(path=path_tourney, name=str(current_image))
            except:
                pass
            
        ext = get_ext_at_file(image.filename)
        image.filename = str(uuid.uuid4()) + "." + ext
        
        upfile(file=image, path=path_tourney)
        db_tourney.image = image.filename
    
    try:
        db.add(db_tourney)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail=_(locale, "tourney.already_exist"))

def close_one_tourney(request: Request, tourney_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    one_status_end = get_one_status_by_name('FINALIZED', db=db)
    
    db_tourney = get_one(tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
    
    if db_tourney.status_id == one_status_end.id:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.tourney_closed"))
    
    # en dependencia de la modalidad organizar la tabla de resultados.
    
    db_tourney.updated_by = currentUser['username']
    db_tourney.updated_date = datetime.now()
    
    db_tourney.status_id = one_status_end.id
    
    # si tengo una ronda creada en estado de configurada o creada debo borrarlas
    str_delete = "Update events.domino_rounds SET status_id = 3 " + \
        "Where tourney_id = '" + db_tourney.id + "' and (status_id = 10 or status_id = 1); COMMIT;"
    db.execute(str_delete)
    
    # calcular al final
    
    try:
        db.add(db_tourney)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail=_(locale, "tourney.already_exist"))
        
def update_image_tourney(request: Request, tourney_id: str, file: File, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request) 
    
    one_status_end = get_one_status_by_name('FINALIZED', db=db)
    
    db_tourney = get_one(tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
    
    if db_tourney.status_id == one_status_end.id:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.tourney_closed"))
    
    db_tourney.updated_by = currentUser['username']
    db_tourney.updated_date = datetime.now()
    
    path_tourney = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(db_tourney.id))
    
    #puede venir la foto o no venir y eso es para borrarla.
    if db_tourney.image:  # ya tiene una imagen asociada
        current_image = db_tourney.image
        try:
            del_image(path=path_tourney, name=str(current_image))
        except:
            pass
    
    if not file:
        db_tourney.image = None
    else:   
        ext = get_ext_at_file(file.filename)
        file.filename = str(uuid.uuid4()) + "." + ext
        
        upfile(file=file, path=path_tourney)
        db_tourney.image = file.filename
    
    try:
        db.add(db_tourney)
        db.commit()
        return result
    except (Exception, SQLAlchemyError) as e:
        print(e.code)
        if e.code == "gkpj":
            raise HTTPException(status_code=400, detail=_(locale, "tourney.already_exist"))

def create_category_by_default(tourney_id:str, elo_max: float, elo_min: float, amount_players: int, db:Session):
    
    #borrar las que existen primero
    str_delete = "DELETE FROM events.domino_categories WHERE tourney_id = '" + tourney_id + "'; COMMIT; "
    db.execute(str_delete)
    
    if not amount_players:
        amount_players = get_count_players_by_tourney(tourney_id, db=db)
    
    db_one_category = DominoCategory(id=str(uuid.uuid4()), tourney_id=tourney_id, category_number=1,
                                    position_number=1, elo_min=elo_min, elo_max=elo_max, 
                                    amount_players=amount_players, by_default=True) 
        
    db.add(db_one_category)
    
    db.commit()    
   
    return True

def created_segmentation_by_level(tourney_id:str, db:Session):
    
    str_query_cat = "Select ps.level, count(*) from events.players_users pu " +\
        "join enterprise.profile_single_player ps ON ps.profile_id = pu.profile_id where player_id IN (" +\
        "Select id from events.players where tourney_id = '" + tourney_id + "') group by ps.level"
    lst_cat = db.execute(str_query_cat)
    
    dict_cat = {'rookie': 3, 'professional': 2, 'expert': 1}
    dict_cat_name = {'rookie': 'TRES', 'professional': 'DOS', 'expert': 'UNO'}
    
    for item in lst_cat:
        level_type = item.level if item.level != 'NORMAL' else 'rookie'
        str_cat_id = "Select id from events.domino_categories where tourney_id = '" + \
            tourney_id + "' and category_number = '" + str(dict_cat_name[level_type]) + "'"
        category_id = db.execute(str_cat_id).fetchone()
        
        category_id = category_id[0] if category_id else None
        category_number = str(dict_cat_name[level_type])
        position_number = dict_cat[level_type]
        
        if not category_id:
            id=str(uuid.uuid4())
            amount_players = update_cat_at_level_for_player(tourney_id, id, level_type, position_number, db=db)
            
            db_one_category = DominoCategory(id=id, tourney_id=tourney_id, category_number=category_number,
                                             position_number=position_number, elo_min=0, elo_max=0, 
                                             amount_players=amount_players, by_default=False) 
        
            db.add(db_one_category)
        else:
            amount_players = update_cat_at_level_for_player(tourney_id, category_id, level_type, position_number, db=db)
            str_update_cat = "Update events.domino_categories cat SET amount_players = " + str(amount_players) +\
                " where id = '" + category_id + "';"
            db.execute(str_update_cat)
   
    db.commit()     
    return True

def update_cat_at_level_for_player(tourney_id: str, category_id: str, level: str, position_number: int, db:Session):
    
    str_result_update = "UPDATE events.players_users pu SET level = '" + level + "', category_id = '" +\
        category_id + "', category_number = " + str(position_number) + " FROM enterprise.profile_single_player ps " +\
        "Where ps.profile_id = pu.profile_id and  player_id IN (" +\
        "Select id from events.players where tourney_id = '" + tourney_id + "') and ps.level = '" + level +\
        "' RETURNING pu.profile_id" 
    lst_result_update = db.execute(str_result_update)
    amount_players = 0
    for item_res in lst_result_update:
        amount_players += 1
    return amount_players

def update_cat_at_elo_for_player(tourney_id: str, db:Session):
    
    str_query_not_cat = "Select pu.elo, pu.player_id, pu.profile_id FROM events.players_users pu join events.players pp ON " +\
        "pp.id = pu.player_id WHERE pp.tourney_id = '" + tourney_id + "' and pu.category_id is NULL "
    lst_result = db.execute(str_query_not_cat)
    for item_pp in lst_result:
        str_cat = "Select id, position_number from events.domino_categories Where tourney_id = '" + tourney_id + "' and elo_max >= " +\
            str(item_pp.elo) + "order by elo_min limit 1 "
        cat_id = db.execute(str_cat).fetchone()
        if not cat_id:
            str_cat = "Select id, position_number from events.domino_categories Where tourney_id = '" + tourney_id + "' " +\
                "order by elo_min limit 1 "
            cat_id = db.execute(str_cat).fetchone()
        
        if not cat_id:
            continue
        category_id = cat_id[0] if cat_id else ''  
        position_number = cat_id[1] if cat_id else 0  
        
        str_result_update = "UPDATE events.players_users pu SET category_id = '" +\
            category_id + "', category_number = " + str(position_number) + " FROM events.players pp " +\
            "Where pp.id = pu.player_id and  pp.tourney_id = '" + tourney_id + "' and pu.profile_id = '" + item_pp.profile_id +\
            "' "
        db.execute(str_result_update)
    
    db.commit()
       
    return True
               
def get_amount_tables(request: Request, tourney_id: str, db: Session): 
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject()
    
    db_tourney = get_one(tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
    
    result.data = calculate_amount_tables(tourney_id, db_tourney.modality, db=db)
    
    return result

def calculate_amount_tables(tourney_id: str, modality: str, db: Session):
    
    amount_players = calculate_amount_players_playing(tourney_id, db=db)
    if amount_players == 0:
        return int(0)
    
    if modality == 'Individual':
        mod_play = divmod(int(amount_players),4) 
    elif modality == 'Parejas':
        mod_play = divmod(int(amount_players),2) 
    elif modality == 'Equipo':
        mod_play = divmod(int(amount_players),2) 
    
    if not mod_play:
        return int(0)
    
    #esta forma es si no voy a dejar mesas incompleta y si jugadores esperando
    # amount_table = int(mod_play[0]) if mod_play[1] > 0 else int(mod_play[0])
     #esta otra sienta a todos los jugadores en las mesas
    amount_table = int(mod_play[0]) if mod_play[1] == 0 else int(mod_play[0] + 1)
    return amount_table

def reconfig_amount_tables(db_tourney, db: Session):

    amount_players = calculate_amount_players_playing(db_tourney.id, db=db)
    if amount_players == 0:
        return int(0)
    
    if db_tourney.modality == 'Individual':
        mod_play = divmod(int(amount_players),4) 
    elif db_tourney.modality == 'Parejas':
        mod_play = divmod(int(amount_players),2) 
    elif db_tourney.modality == 'Equipo':
        mod_play = divmod(int(amount_players),2) 
    
    amount_table = int(mod_play[0]) if mod_play[1] > 0 else int(mod_play[0])
    amount_player_waiting = int(mod_play[1]) if mod_play[1] > 0 else 0
    
    if amount_table != db_tourney.amount_tables:
        if amount_table > db_tourney.amount_tables: # crear mas mesas
            amount_trad_tables = db_tourney.amount_tables - amount_table
            table_number = db_tourney.amount_tables
            for i in range(amount_trad_tables):
                table_number += 1
                created_one_domino_tables(db_tourney, table_number, False, 0, db=db, created_by=db_tourney.updated_by, file=None)
        else:
            amount_trad_tables = db_tourney.amount_tables - amount_table
            # quitralas
            
    return amount_table, amount_player_waiting

def calculate_amount_categories(tourney_id: str, db: Session):
    
    str_query = "Select count(*) From events.domino_categories Where by_default is False and tourney_id = '" + tourney_id + "' "
    amount_category = db.execute(str_query).fetchone()[0]
    return int(amount_category)

def calculate_amount_players_playing(tourney_id: str, db: Session):
    
    str_query = "Select count(*) From events.players player " + \
        "JOIN resources.entities_status sta ON sta.id = player.status_id " +\
        "Where tourney_id = '" + tourney_id + "' " +\
        "AND sta.name IN ('CONFIRMED', 'PLAYING', 'WAITING') "
    amount_play = db.execute(str_query).fetchone()[0]
    return int(amount_play)

def get_number_players_by_elo(tourney_id:str, min_elo:float, max_elo:float, db:Session):  
    str_query = "Select count(*) From events.players player " + \
        "JOIN resources.entities_status sta ON sta.id = player.status_id " +\
        "Where tourney_id = '" + tourney_id + "' " +\
        "AND sta.name IN ('CONFIRMED', 'PLAYING', 'WAITING') " +\
        "AND player.elo >= " + str(min_elo) + " AND player.elo <= " + str(max_elo)
    amount_play = db.execute(str_query).fetchone()[0]
    return int(amount_play)
    
def calculate_amount_players_by_status(tourney_id: str, status_name: str, db: Session):
    
    str_query = "Select count(*) From events.players play JOIN resources.entities_status sta ON " +\
        "sta.id = play.status_id Where tourney_id = '" + tourney_id + "' " +\
        "AND sta.name = '" + str(status_name) + "' "
    amount_play = db.execute(str_query).fetchone()[0]
    return int(amount_play)

def calculate_elo_by_tourney(tourney_id: str, modality:str, db: Session):
    
    amount_players = calculate_amount_players_playing(tourney_id=tourney_id, db=db)
    
    if amount_players == 0:
        return int(0)
    
    if modality == 'Individual':
        mod_play = divmod(int(amount_players),4) 
    elif modality == 'Parejas':
        mod_play = divmod(int(amount_players),2) 
    elif modality == 'Equipo':
        mod_play = divmod(int(amount_players),2) 
    
    if not mod_play:
        return int(0)
    
    return int(mod_play[0]) + 1 if mod_play[1] > 0 else int(mod_play[0])

def get_lst_categories_of_tourney(tourney_id: str, db: Session):
    
    lst_categories = []
    
    str_query = "SELECT id, category_number, position_number, elo_min, elo_max, amount_players " +\
        "FROM events.domino_categories WHERE by_default is False and tourney_id = '" + tourney_id + "' Order by elo_max DESC "
        
    lst_all_category = db.execute(str_query).fetchall()
    for item in lst_all_category:
        lst_categories.append(
            {'id': item.id, 'category_number': item.category_number, 'position_number': item.position_number,
             'amount_players': item.amount_players, 'elo_min': item.elo_min, 'elo_max': item.elo_max})
    return lst_categories

def get_categories_of_tourney(tourney_id: str, db: Session):
    return db.query(DominoCategory).filter(DominoCategory.tourney_id == tourney_id).all()

def get_one_category_by_id(category_id: str, db: Session):
    return db.query(DominoCategory).filter(DominoCategory.id == category_id).first()

# def initializes_tourney(tourney_id, amount_tables, amount_smart_tables, amount_rounds, number_points_to_win, 
#                         time_to_win, game_system, use_bonus, lottery_type, penalties_limit, db: Session):
    
#     amount_bonus_tables = amount_rounds // 4 
#     divmod_round = divmod(amount_rounds,5)
#     number_bonus_round = amount_rounds + 1 if amount_rounds <= 9 else 4 if amount_rounds <= 15 else \
#         divmod_round[0] if divmod_round[1] == 0 else divmod_round[0] + 1
#     amount_bonus_points = amount_bonus_tables * 2
    
#     sett_tourney = SettingTourney(amount_tables=amount_tables, amount_smart_tables=amount_smart_tables, 
#                                   amount_rounds=amount_rounds, use_bonus=use_bonus,
#                                   amount_bonus_tables=amount_bonus_tables, amount_bonus_points=amount_bonus_points, 
#                                   number_bonus_round=number_bonus_round, 
#                                   number_points_to_win=number_points_to_win, time_to_win=time_to_win, 
#                                   game_system=game_system, lottery_type=lottery_type, penalties_limit=penalties_limit)
    
#     sett_tourney.tourney_id = tourney_id
    
#     try:
#         db.add(sett_tourney)
#         db.commit()
#         return True
       
#     except (Exception, SQLAlchemyError, IntegrityError) as e:
#         return False
    
# def init_setting(tourney_id, modality, db: Session):
    
#     amount_tables = calculate_amount_tables(tourney_id, modality=modality, db=db)
#     elo_max, elo_min = get_values_elo_by_tourney(tourney_id=tourney_id, modality=modality, db=db)
    
#     sett_tourney = SettingTourney(
#         amount_tables=amount_tables, amount_smart_tables=0, amount_rounds=0, use_bonus=False, amount_bonus_tables=0, 
#         amount_bonus_points=0, number_bonus_round=0, number_points_to_win=0, time_to_win=0, 
#         game_system='', lottery_type='', penalties_limit=0, elo_min=elo_min, elo_max=elo_max, image='')
    
#     sett_tourney.tourney_id = tourney_id
    
#     try:
#         db.add(sett_tourney)
#         db.commit()
#         return sett_tourney
       
#     except (Exception, SQLAlchemyError, IntegrityError) as e:
#         return None

#metodo viejo, ya se piede borrar
# def configure_categories_tourney(request, tourney_id: str, lst_categories: List[DominoCategoryCreated], db: Session):
#     locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
#     result = ResultObject() 
    
#     db_tourney = get_one(tourney_id, db=db)
#     if not db_tourney:
#         raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
   
#     status_created = get_one_status_by_name('FINALIZED', db=db)
    
#     if db_tourney.status_id == status_created.id:
#         raise HTTPException(status_code=404, detail=_(locale, "tourney.is_configurated"))
    
#     str_query = "SELECT count(tourney_id) FROM events.domino_categories where tourney_id = '" + tourney_id + "' "
#     amount = db.execute(str_query).fetchone()[0]
#     if amount > 0:  #borrar todo lo que esta salvado y poner siempre nuevo...
#         str_delete = "DELETE FROM events.domino_categories Where tourney_id = '" + tourney_id + "'; COMMIT; "
#         db.execute(str_delete)
    
#     position_number = 0
#     for item in lst_categories:
#         position_number += 1
#         db_one_category = DominoCategory(id=str(uuid.uuid4()), tourney_id=tourney_id, category_number=item.category_number,
#                                          position_number=position_number, elo_min=item.elo_min, elo_max=item.elo_max,
#                                          amount_players=item.amount_players if item.amount_players else 0) 
        
#         db.add(db_one_category)
    
#     try:
#         db.commit()
#         return result
#     except (Exception, SQLAlchemyError, IntegrityError) as e:
#         return result
    
def insert_categories_tourney(request, tourney_id: str, categories: DominoCategoryCreated, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    db_tourney = get_one(tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
   
    if db_tourney.status.name == 'FINALIZED':
        raise HTTPException(status_code=404, detail=_(locale, "tourney.is_configurated"))
    
    categories.category_type = 'ELO'
    if categories.category_type == 'ELO':
        result.data = insert_player_by_elo_category(locale, tourney_id, categories, db=db)
        return result
    elif categories.category_type == 'LEVEL':
        result.data = insert_player_by_level_category(locale, tourney_id, categories, db=db)
    elif categories.category_type == 'LEVEL':
        result.data = insert_player_by_level_category(locale, tourney_id, categories, db=db)
        
    return result
    # except (Exception, SQLAlchemyError, IntegrityError) as e:
    #     return result

def insert_player_by_elo_category(locale, tourney_id: str, categories: DominoCategoryCreated, db: Session):
    
    position_number, elo_min, by_default = 0, 0, False
    str_query = "SELECT position_number, elo_min, by_default FROM events.domino_categories where tourney_id = '" + tourney_id + "' " +\
        "ORDER BY elo_min DESC limit 1 "
    lst_info = db.execute(str_query).fetchone()
    if lst_info:
        position_number = lst_info[0]
        elo_min = lst_info[1]
        by_default = lst_info[2]

    if by_default:  
        str_delete = "DELETE FROM events.domino_categories where tourney_id = '" + tourney_id + "'; COMMIT; "
        lst_info = db.execute(str_delete)
    else:
        if elo_min and categories.elo_max >= elo_min:
            raise HTTPException(status_code=404, detail=_(locale, "tourney.elo_max_incorrect"))
    
    status_canc = get_one_status_by_name('CANCELLED', db=db)    
    str_query = "SELECT count(player.id) FROM events.players player WHERE status_id != " + str(status_canc.id)
    str_query += " AND player.tourney_id = '" + tourney_id + "' "  +\
        "AND player.elo >= " + str(categories.elo_min) + " AND player.elo <= " + str(categories.elo_max)
    amount_players = db.execute(str_query).fetchone()[0]
    if amount_players <= 0:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.category_not_player"))
    
    position_number += 1
    db_one_category = DominoCategory(id=str(uuid.uuid4()), tourney_id=tourney_id, category_number=categories.category_number,
                                     position_number=position_number, elo_min=categories.elo_min, elo_max=categories.elo_max,
                                     amount_players=amount_players, by_default=False) 
    
    db.add(db_one_category)
    db.commit()
    
    # marcar a los jugadores en ella contenidos
    str_query = "SELECT player.id FROM events.players player WHERE status_id != " + str(status_canc.id)
    str_query += " AND player.tourney_id = '" + tourney_id + "' "  +\
        "AND player.elo >= " + str(categories.elo_min) + " AND player.elo <= " + str(categories.elo_max)
    lst_players = db.execute(str_query)
    str_player = ""
    for item_pa in lst_players:  
        str_player += "'" + item_pa.id + "',"
    
    if str_player:    
        str_player = str_player[:-1] if str_player else str_player
        update_category_at_players(db_one_category.id, db_one_category.position_number, str_player, db=db)
    
    return True
    
def update_category_at_players(category_id:str, category_number:int, str_players: str, db:Session):
    
    str_update = "UPDATE events.players_users SET category_id='" + category_id +\
        "', category_number=" + str(category_number) + " WHERE player_id IN (" + str_players + "); COMMIT;"
    db.execute(str_update)
    
    db.commit()
    
    return True

def insert_player_by_level_category(locale, tourney_id: str, categories: DominoCategoryCreated, db: Session):
    
    position_number, elo_min, by_default = 0, 0, False
    str_query = "SELECT position_number, elo_min, by_default FROM events.domino_categories where tourney_id = '" + tourney_id + "' " +\
        "ORDER BY elo_min DESC limit 1 "
    lst_info = db.execute(str_query).fetchone()
    if lst_info:
        position_number = lst_info[0]
        elo_min = lst_info[1]
        by_default = lst_info[2]

    if by_default:  
        str_delete = "DELETE FROM events.domino_categories where tourney_id = '" + tourney_id + "'; COMMIT; "
        lst_info = db.execute(str_delete)
    else:
        if elo_min and categories.elo_max >= elo_min:
            raise HTTPException(status_code=404, detail=_(locale, "tourney.elo_max_incorrect"))
    
    status_canc = get_one_status_by_name('CANCELLED', db=db)    
    str_query = "SELECT count(player.id) FROM events.players player WHERE status_id != " + str(status_canc.id)
    str_query += " AND player.tourney_id = '" + tourney_id + "' "  +\
        "AND player.elo >= " + str(categories.elo_min) + " AND player.elo <= " + str(categories.elo_max)
    amount_players = db.execute(str_query).fetchone()[0]
    
    if amount_players <= 1:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.category_not_player"))
    
    position_number += 1
    db_one_category = DominoCategory(id=str(uuid.uuid4()), tourney_id=tourney_id, category_number=categories.category_number,
                                     position_number=position_number, elo_min=categories.elo_min, elo_max=categories.elo_max,
                                     amount_players=amount_players, by_default=False) 
    
    db.add(db_one_category)
    
    # try:
    db.commit()
    return True
    # except (Exception, SQLAlchemyError, IntegrityError) as e:
    #     return False
        
def update_amount_player_by_categories(tourney_id: str, db: Session):
    
    lst_categories = get_categories_of_tourney(tourney_id, db=db)
    for item in lst_categories:
        item.amount_players = get_number_players_by_elo(tourney_id, item.elo_min, item.elo_max, db=db)
        db.add(item)
    
    # try:
    db.commit()
    return True
    # except (Exception, SQLAlchemyError, IntegrityError) as e:
    #     return result
    
def delete_categories_tourney(request, category_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    db_category = get_one_category_by_id(category_id, db=db)
    if not db_category:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.category_not_exist"))
        
    if db_category.tourney.status.name == 'FINALIZED':
        raise HTTPException(status_code=404, detail=_(locale, "tourney.is_configurated"))
    
    # try:
        
    str_update = "UPDATE events.players_users SET category_id=NULL, category_number=NULL" +\
            " WHERE category_id='" + db_category.id + "'; COMMIT;"
    db.execute(str_update)
    db.delete(db_category)
    db.commit()
    return result
    # except (Exception, SQLAlchemyError, IntegrityError) as e:
    #     return result

def get_all_categories_tourney(request:Request, tourney_id: str, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    result.data = get_list_categories_tourney(tourney_id=tourney_id, db=db)
    # if not result.data:
    #     raise HTTPException(status_code=404, detail=_(locale, "tourney.categories_not_exist"))
        
    return result

def get_list_categories_tourney(tourney_id: str, db: Session):
    
    str_query = "SELECT * FROM events.domino_categories where by_default is False AND tourney_id = '" + tourney_id + "' ORDER BY position_number"
    lst_cat = db.execute(str_query).fetchall()
    lst_data = []
    for item in lst_cat:
        lst_data.append({'id': item.id, 'category_number': item.category_number, 'elo_min': item.elo_min, 'elo_max': item.elo_max,
                         'amount_players': item.amount_players})
    
    return lst_data

def get_info_categories_tourney(category_id: str, db: Session):
    
    str_query = "SELECT cat.id, cat.tourney_id, tourney.modality, cat.elo_min, cat.elo_max, tourney.lottery_type, " +\
        "st.name as status_name, cat.amount_players, tourney.segmentation_type " +\
        "FROM events.domino_categories cat JOIN events.tourney ON " +\
        "tourney.id = cat.tourney_id JOIN resources.entities_status st ON st.id = tourney.status_id " +\
        "where cat.id = '" + category_id + "' "
    lst_cat = db.execute(str_query).fetchall()
    
    dict_result = {}
    for item in lst_cat:
        dict_result = {'id': item.id, 'tourney_id': item.tourney_id, 'modality': item.modality, 
                       'elo_min': item.elo_min, 'elo_max': item.elo_max, 'lottery_type': item.lottery_type,
                       'status_name': item.status_name, 'amount_players': item.amount_players,
                       'segmentation_type': item.segmentation_type}
    
    return dict_result

def get_one_domino_category(category_id: str, db: Session):
    return db.query(DominoCategory).filter(DominoCategory.id == category_id).first()

def get_str_to_order(db_tourney):
    
    str_order_by = "" 
    # dict_order = {'JG': 'games_won ',
    #               'ERA': 'elo_ra ',
    #               'DP': 'points_difference ',
    #               'JJ': 'games_played ',
    #               'PF': 'points_positive ',
    #               'ELO': 'elo_at_end '}
    
    dict_order = {'JG': 'rsca.acumulated_games_won ',
                  'ERA': 'rsca.elo_ra ',
                  'DP': 'rsca.acumulated_points_positive-rsca.acumulated_points_negative ',
                  'JJ': 'rsca.acumulated_games_played ',
                  'PF': 'rsca.acumulated_points_positive ',
                  'ELO': 'rsca.acumulated_elo_variable '}
    
    # En el evento no tengo en cuenta la
    # str_order_by = " ORDER BY category_number ASC, " if db_tourney.use_segmentation else " ORDER BY " 
    
    str_order_by = " ORDER BY "
    if db_tourney.event_ordering_one:
        str_order_by += dict_order[db_tourney.event_ordering_one] + db_tourney.event_ordering_dir_one
    
    if db_tourney.event_ordering_two:
        str_order_by += ", " + dict_order[db_tourney.event_ordering_two] + db_tourney.event_ordering_dir_two
        
    if db_tourney.event_ordering_three:
        str_order_by += ", " + dict_order[db_tourney.event_ordering_three] + db_tourney.event_ordering_dir_three
    
    return str_order_by
    
def save_image_tourney(request, tourney_id: str, file: File, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    db_tourney = get_one(tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
    
    path = create_dir(entity_type="SETTOURNEY", user_id=None, entity_id=str(db_tourney.id))
    
    # si torneo tiene imagen ya, eliminarla primero
    if db_tourney.image:
        try:
            del_image(path, db_tourney.image)
        except:
            pass
    
    image_id=str(uuid.uuid4())
    if file:
        ext = get_ext_at_file(file.filename)
        file.filename = str(image_id) + "." + ext
        db_tourney.image = file.filename
        upfile(file=file, path=path)
    else:
        image_domino="public/smartdomino.png"
        filename = str(image_id) + ".png"
        image_destiny = path + filename
        copy_image(image_domino, image_destiny)
        db_tourney.image = filename
     
    try:
        db.add(db_tourney)
        
        db.commit()
        return result
        
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        return result
 
    return result
   
def get_values_elo_by_tourney(tourney_id: str, db: Session):  
    
    status_canc = get_one_status_by_name('CANCELLED', db=db)
    
    str_from = "FROM events.players player " +\
        "inner join enterprise.profile_member pro ON pro.id = player.profile_id " +\
        "join resources.entities_status sta ON sta.id = player.status_id "
    
    str_query = "SELECT MAX(elo) elo_max, MIN(elo) elo_min " + str_from
    
    str_where = "WHERE pro.is_ready is True AND status_id != " + str(status_canc.id) 
    str_where += " AND player.tourney_id = '" + tourney_id + "' "  
    
    str_query += str_where

    lst_data = db.execute(str_query)
    elo_max, elo_min = float(0.00), float(0.00)
    for item in lst_data:
        elo_max = item.elo_max
        elo_min = item.elo_min
    
    return elo_max, elo_min

def get_factor_scale():
    
    K1 = 16 # por ahora será fijo en 4 hasta que me digan bien la formula
    
    return K1

def get_all_accumulated_scale_by_tourney(request:Request, page: int, per_page: int, tourney_id: str, db: Session):  
    
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    api_uri = str(settings.api_uri)
    
    str_from = "FROM events.players_users rsca " +\
        "JOIN events.players players ON players.id = rsca.player_id " +\
        "JOIN enterprise.profile_member mmb ON players.profile_id = mmb.id " 
        
    str_count = "Select count(*) " + str_from
    str_query = "SELECT players.id player_id, mmb.id profile_id, mmb.name profile_name, mmb.photo, rsca.games_played, " +\
        "rsca.elo, rsca.elo_current, rsca.penalty_total penalty_points, rsca.games_won,  rsca.games_lost, points_difference, " +\
        "rsca.points_positive, rsca.points_negative, rsca.score_expected, score_obtained, k_value, elo_at_end, " +\
        "bonus_points, position_number_at_end " + str_from
    
    str_where = "WHERE players.tourney_id = '" + tourney_id + "' "
    
    str_count += str_where
    str_query += str_where + " ORDER BY position_number_at_end "

    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    if page != 0:
        str_query += " LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(str_query)
    
    result.data = []
    for item in lst_data:
        result.data.append(create_dict_row_scale_acum(item, api_uri=api_uri))
    
    return result
    
def create_dict_row_scale_acum(item, api_uri):
    
    photo = get_url_avatar(item['profile_id'], item['photo'], api_uri=api_uri)
    
    new_row = {'id': item['player_id'], 'name': item['profile_name'], 
               'position_number': item.position_number_at_end,
               'photo' : photo, 'elo': format_number(round(item['elo'],2)) if item['elo'] else 0, 
               'elo_variable': format_number(round(item['elo_current'],2)) if item['elo_current'] else 0,
               'elo_at_end': format_number(round(item['elo_at_end'],2)),   
               'games_played': item['games_played'], 
               'games_won': item['games_won'] if item['games_won'] else 0,
               'games_lost': item['games_lost'] if item['games_lost'] else 0, 
               'points_positive': item['points_positive'] if item['points_positive'] else 0,
               'points_negative': item['points_negative'] if item['points_negative'] else 0, 
               'points_difference': item['points_difference'],
               'penalty_points': item['penalty_points'] if item['penalty_points']  else 0,
               'penalty_total': item['penalty_points'] if item['penalty_points']  else 0,
               'score_expected': format_number(round(item['score_expected'],2)) if item['score_expected'] else 0,
               'score_obtained': format_number(round(item['score_obtained'],2)) if item['score_obtained'] else 0,
               'k_value': format_number(round(item['k_value'],2)) if item['k_value'] else 0,
               'elo_at_end': format_number(round(item['elo_at_end'],2)) if item['elo_at_end'] else 0,
               'bonus_points': 0}
    
    return new_row