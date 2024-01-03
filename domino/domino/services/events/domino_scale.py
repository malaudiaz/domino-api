import math
import uuid
import random

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

from domino.models.events.domino_round import DominoRoundsScale, DominoRoundsPairs
from domino.models.events.tourney import TraceLotteryManual

from domino.schemas.events.domino_rounds import DominoManualScaleCreated, DominoRoundsAperture
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.resources.status import get_one_by_name as get_one_status_by_name, get_one as get_one_status
from domino.services.resources.utils import get_result_count, upfile, create_dir, del_image, get_ext_at_file, remove_dir
from domino.services.enterprise.userprofile import get_one as get_one_profile
from domino.services.enterprise.auth import get_url_avatar

from domino.services.events.player import get_lst_id_player_by_elo
from domino.services.events.domino_round import get_one as get_one_round, get_first_by_tourney, configure_rounds, configure_new_rounds, \
    get_obj_info_to_aperturate
    
from domino.services.events.domino_boletus import created_boletus_for_round
from domino.services.enterprise.auth import get_url_advertising
from domino.services.events.tourney import get_lst_categories_of_tourney

from domino.services.events.calculation_serv import calculate_new_elo
    
def new_initial_manual_round(request: Request, tourney_id:str, dominoscale: list[DominoManualScaleCreated], db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    result = ResultObject() 
    
    currentUser = get_current_user(request) 
    
    round_id, modality = get_round_to_configure(locale, tourney_id, db=db)
    one_status_init = get_one_status_by_name('INITIADED', db=db)
    
    initial_scale_by_manual_lottery(tourney_id, round_id, dominoscale, modality, db=db)
    
    configure_tables_by_round(tourney_id, round_id, modality, currentUser['username'], db=db)
    
    # cambiar estado del torneo a Iniciado
    str_update = "UPDATE events.tourney SET status_id=" + str(one_status_init.id) + " WHERE id = '" + tourney_id + "';"
    str_update += "UPDATE events.events SET status_id=" + str(one_status_init.id) + " WHERE id IN " +\
        "(Select tourney.event_id FROM events.tourney where id = '" + tourney_id + "');COMMIT;"
    db.execute(str_update)
    
    return result

def configure_tables_by_round(tourney_id:str, round_id: str, modality:str, created_by:str, db: Session, round_number:int=1):
    
    if round_number == 1:
        update_elo_initial_scale(tourney_id, round_id, modality, db=db)
    
    #configurar parejas y rondas
    configure_rounds(tourney_id=tourney_id, round_id=round_id, modality=modality, created_by=created_by, db=db)
    
    #ubicar por mesas las parejas
    created_boletus_for_round(tourney_id=tourney_id, round_id=round_id, db=db)
    
    return True

def get_round_to_configure(locale, tourney_id:str, db: Session):
    
    # si el torneo ya tiene mas de una ronda no se puede hacer esto
    str_query = "Select count(*) FROM events.domino_rounds WHERE tourney_id = '" + tourney_id + "' "
    amount_round = db.execute(str_query).fetchone()[0]
    if amount_round != 1:
        raise HTTPException(status_code=404, detail=_(locale, "round.not_initial_round"))
    
    str_query = "Select id FROM events.domino_rounds WHERE tourney_id = '" + tourney_id + "' and round_number = 1 "
    round_id = db.execute(str_query).fetchone()
    if not round_id:
        raise HTTPException(status_code=404, detail=_(locale, "round.not_initial_round"))
    
    str_query = "Select modality FROM events.tourney WHERE id = '" + tourney_id + "' "
    modality = db.execute(str_query).fetchone()
    if not modality:
        raise HTTPException(status_code=404, detail=_(locale, "round.not_initial_round"))
    
    return round_id[0], modality[0]

def update_elo_initial_scale(tourney_id: str, round_id: str, modality:str, db: Session ):
    
    str_scale = "Select player_id from events.domino_rounds_scale where tourney_id = '" + tourney_id + "' " +\
        "and round_id = '" + round_id + "' order by position_number ASC "
    
    lst_scale = db.execute(str_scale).fetchall()
    
    str_select = "Select Round(SUM(elo)/2,4) as elo " if modality == 'Parejas' else 'Select elo '
    str_select += "FROM events.players play JOIN enterprise.profile_users puse ON puse.profile_id = play.profile_id " +\
        "JOIN enterprise.profile_single_player splay ON splay.profile_id = puse.single_profile_id "
    
    str_update = "UPDATE events.domino_rounds_scale SET elo = "
    str_all_update = ''
    for item in lst_scale:
        str_find = str_select + " where id = '" + item.player_id + "' "
        elo = db.execute(str_find).fetchone()
        if elo:
            str_one_update = str_update + str(elo[0]) + " where player_id = '" + item.player_id + "'; "
            str_all_update += str_one_update
    
    if str_all_update:
        db.execute(str_all_update)
        db.commit()
        
    return True

def create_one_scale(tourney_id: str, round_id: str, round_number, position_number: int, player_id: str, category_id:str, db: Session, 
                     elo:float=None):
    one_scale = DominoRoundsScale(id=str(uuid.uuid4()), tourney_id=tourney_id, round_id=round_id, round_number=round_number, 
                                  position_number=int(position_number), player_id=player_id, is_active=True, category_id=category_id,
                                  elo=elo)
    db.add(one_scale)
        
    return True

def create_one_manual_trace(tourney_id: str, modality:str, position_number: int, player_id: str, db: Session ):
    
    one_trace = TraceLotteryManual(id=str(uuid.uuid4()), tourney_id=tourney_id, modality=modality, 
                                   position_number=int(position_number), player_id=player_id, is_active=True)
    db.add(one_trace)
        
    return True

def initial_scale_by_manual_lottery(tourney_id: str, round_id: str, dominoscale:list, modality:str, db: Session):
    
    for item in dominoscale:
        create_one_manual_trace(tourney_id, modality, int(item['position_number']), item['id'], db=db)
        create_one_scale(tourney_id, round_id, 1, int(item['position_number']), item['id'], category_id=item['category'], db=db)
    db.commit()
    return True


def configure_automatic_lottery(db_round, db: Session):
    
    # buscar las categorias definidas. 
    str_query = "SELECT * FROM events.domino_categories where tourney_id = '" + db_round.tourney.id + "' ORDER BY position_number "
    lst_categories = db.execute(str_query).fetchall()
    
    position_number=0
    for item_cat in lst_categories:   
        position_number=created_automatic_lottery(
            db_round.tourney.id, db_round.tourney.modality, db_round.id, item_cat.elo_min, item_cat.elo_max, position_number, item_cat.id, db=db)
   
    return True

def created_automatic_lottery(tourney_id: str, modality:str, round_id: str, elo_min:float, elo_max:float, position_number:int, category_id, db: Session):
    
    list_player = get_lst_id_player_by_elo(tourney_id, modality, min_elo=elo_min, max_elo=elo_max, db=db)
    
    lst_groups = sorted(list_player, key=lambda y:random.randint(0, len(list_player)))
    for item_pos in lst_groups:
        position_number += 1
        create_one_scale(tourney_id, round_id, 1, position_number, item_pos, category_id, db=db)
    db.commit()
    return position_number

def configure_new_lottery_by_round(db_round, db_round_new, modality:str, db: Session):
    
    # buscar las categorias definidas. 
    str_query = "SELECT * FROM events.domino_categories where tourney_id = '" + db_round.tourney_id + "' ORDER BY position_number"
    lst_categories = db.execute(str_query).fetchall()
    
    position_number = 0
    for item_cat in lst_categories:  
        position_number=created_automatic_lottery_by_round_cat(
            db_round.tourney_id, db_round.id, db_round_new.id, db_round_new.round_number, item_cat.id, position_number, db=db)
        
    configure_tables_by_round(db_round.tourney_id, db_round_new.id, modality, db_round.created_by, db=db)
    
    db.commit()
    
    return True

def close_round_with_verify(db_round: str, status_end, username: str, db: Session):
    
    str_count = "SELECT count(id) FROM events.domino_boletus Where round_id = '" + db_round.id + "' AND status_id != " + str(status_end.id)
    
    # verificar si ya todas las boletas cerraron, debemos cerrar la ronda.
    amount_boletus = db.execute(str_count).fetchone()[0]
    if amount_boletus != 0:
        return {'closed_round': False}
    
    db_round.close_date = datetime.now()
    
    last_number = db_round.round_number + 1
    
    # crear la nueva ronda
    new_round = configure_new_rounds(db_round.tourney_id, 'Ronda Nro.' + str(last_number), db, created_by=username, round_number=last_number)
    
    configure_new_lottery_by_round(db_round, new_round, db_round.tourney.modality, db=db)
    
    db_round.status_id = status_end.id
    if username:
        db_round.updated_by = username
    db_round.updated_date = datetime.now()
    
    db.add(db_round)
    db.commit()
    
    return {'closed_round': True}

def created_automatic_lottery_by_round_cat(tourney_id: str, round_id: str, new_round_id: str, new_round_number: int, category_id: str, 
                                       position_number:int, db: Session):
    
    list_player, dict_player = get_lst_player_by_scale_category(round_id, category_id, db=db)
    
    lst_groups = sorted(list_player, key=lambda y:random.randint(0, len(list_player)))
    for item_pos in lst_groups:
        position_number += 1
        create_one_scale(tourney_id, new_round_id, new_round_number, position_number, item_pos, category_id, db=db, elo=dict_player[item_pos])
    db.commit()
    return position_number

def get_lst_player_by_scale_category(round_id: str, category_id: str, db: Session):  
    
    str_query = "SELECT player_id, elo_variable FROM events.domino_rounds_scale WHERE is_active = True " +\
        "AND round_id = '" + round_id + "' AND category_id = '" + category_id + "' "
    lst_data = db.execute(str_query)
    dict_player = {}
    lst_players = []
    for item in lst_data:
        lst_players.append(item.player_id)
        dict_player[item.player_id] = item.elo_variable
    
    return lst_players, dict_player

def get_lst_players(tourney_id: str, round_id: str, db: Session):  
    return db.query(DominoRoundsScale).filter(DominoRoundsScale.tourney_id == tourney_id).\
        filter(DominoRoundsScale.round_id == round_id).order_by(DominoRoundsScale.position_number).all()
        
def get_lst_players_with_profile(tourney_id: str, round_id: str, db: Session):  
    
    lst_player = []
    
    str_query = "Select doms.player_id, puser.single_profile_id From events.domino_scale doms " +\
        "join events.players play ON play.id = doms.player_id " +\
        "join enterprise.profile_users puser ON puser.profile_id = play.profile_id " +\
        "Where doms.tourney_id = '" + tourney_id + "' and round_id = '" + round_id + "' "
    lst_result = db.execute(str_query)
    for item in lst_result:
        lst_player.append({'player_id': item.player_id, 'single_profile_id': item.single_profile_id})
    
    return lst_player

def get_all_players_by_tables(request:Request, page: int, per_page: int, tourney_id: str, round_id: str, db: Session):  
    
    # SI LA RONDA VIENE VACIA ES LA PRIMERA DEL TORNEO.
    
    if not round_id:
        db_round = get_first_by_tourney(tourney_id, db=db)
        round_id = db_round.id
    
    return get_all_players_by_tables_and_rounds(request, page, per_page=per_page, tourney_id=tourney_id, round_id=round_id, db=db)
        
def get_all_players_by_tables_and_round(request:Request, page: int, per_page: int, round_id: str, db: Session):  
    
    db_round = get_one_round(round_id, db=db)
    return get_all_players_by_tables_and_rounds(request, page, per_page=per_page, tourney_id=db_round.tourney_id, round_id=round_id, db=db)
    
def get_all_players_by_tables_and_rounds(request:Request, page: int, per_page: int, tourney_id: str, round_id: str, db: Session):  
    
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    api_uri = str(settings.api_uri)
    
    str_from = "FROM events.domino_boletus bol " +\
        "JOIN events.domino_tables dtab ON dtab.id = bol.table_id " +\
        "JOIN events.tourney tou ON tou.id = dtab.tourney_id " 
    
    str_count = "Select count(*) " + str_from
    str_query = "SELECT DISTINCT dtab.id as table_id, dtab.table_number, is_smart, dtab.image as table_image, " +\
        "tou.image as tourney_image, bol.id as boletus_id, dtab.tourney_id " + str_from
        
    str_where = "WHERE bol.is_valid is True AND dtab.is_active is True " + \
        "AND  dtab.tourney_id = '" + tourney_id + "' AND bol.round_id = '" + round_id + "' "
        
    str_count += str_where
    str_query += str_where + " ORDER BY dtab.table_number "

    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(str_query)
    
    lst_tables = []
    id=0
    for item in lst_data:
        
        table_image = get_url_advertising(tourney_id, item['table_image'] if item['table_image'] else item['tourney_image'], api_uri=api_uri)
        
        dict_tables = {'id': id, 'number': int(item['table_number']), 'table_id': item.table_id,
                       'type': "Inteligente" if item['is_smart'] else "Tradicional",
                       'image': table_image}
        
        dict_tables=create_dict_position(dict_tables, item.boletus_id, api_uri, db=db)
        lst_tables.append(dict_tables)
        id+=1
        
    result.data = lst_tables        
            
    return result

def get_all_scale_by_round(request:Request, page: int, per_page: int, round_id: str, db: Session):  
    
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    api_uri = str(settings.api_uri)
    
    str_from = "FROM events.domino_rounds_scale rsca " +\
        "JOIN events.players players ON players.id = rsca.player_id " +\
        "JOIN enterprise.profile_member mmb ON players.profile_id = mmb.id " +\
        "left join resources.city ON city.id = mmb.city_id " +\
        "left join resources.country ON country.id = city.country_id " 
    
    str_count = "Select count(*) " + str_from
    str_query = "SELECT players.id player_id, mmb.id profile_id, mmb.name profile_name, mmb.photo, rsca.position_number, " +\
        "city.name as city_name, country.name as country_name, rsca.elo, rsca.elo_variable, rsca.games_played, " +\
        "rsca.games_won, rsca.games_lost, rsca.points_positive, rsca.points_negative, rsca.points_difference " + str_from
        
    str_where = "WHERE rsca.is_active is True AND rsca.round_id = '" + round_id + "' "
        
    str_count += str_where
    str_query += str_where + " ORDER BY rsca.position_number "

    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data = db.execute(str_query)
    result.data = [create_dict_row_scale(item, db=db, api_uri=api_uri) for item in lst_data]
    
    return result

def create_dict_row_scale(item, db: Session, api_uri):
    
    photo = get_url_avatar(item['profile_id'], item['photo'], api_uri=api_uri)
    
    new_row = {'id': item['player_id'], 'name': item['profile_name'], 
               'position_number': item['position_number'],
               'country': item['country_name'] if item['country_name'] else '', 
               'city_name': item['city_name'] if item['city_name'] else '',  
               'photo' : photo, 'elo': item['elo'] if item['elo'] else 0, 
               'elo_variable': item['elo_variable'] if item['elo_variable'] else 0, 
               'games_played': item['games_played'] if item['games_played'] else 0, 
               'games_won': item['games_won'] if item['games_won'] else 0,
               'games_lost': item['games_lost'] if item['games_lost'] else 0, 
               'points_positive': item['points_positive'] if item['points_positive'] else 0,
               'points_negative': item['points_negative'] if item['points_negative'] else 0, 
               'points_difference': item['points_difference'] if item['points_difference'] else 0}
    
    return new_row

def create_dict_position(dict_tables, boletus_id: str, api_uri:str, db: Session):
    
    str_pos = "SELECT bpos.position_id, pro.name as profile_name, psin.elo, psin.ranking, psin.level, " +\
        "bpos.single_profile_id, pro.photo, bpos.scale_number " +\
        "FROM events.domino_boletus_position bpos " +\
        "JOIN enterprise.profile_single_player psin ON psin.profile_id = bpos.single_profile_id " +\
        "JOIN enterprise.profile_member pro ON pro.id = psin.profile_id " +\
        "WHERE bpos.boletus_id = '" + boletus_id + "' ORDER BY bpos.position_id "
    lst_data = db.execute(str_pos)
    
    for item in lst_data:
        photo = get_url_avatar(item['single_profile_id'], item['photo'], api_uri=api_uri)
        dict_player = {'id': item.position_id, 'name': item.profile_name, 'elo': item.elo, 'nivel': item.level, 
                       'index': item.scale_number if item.scale_number else item.position_id, 'avatar': photo}
        
        if item.position_id == 1:
            dict_tables['playerOne'] = dict_player
        elif item.position_id == 2:  
            dict_tables['playerTwo'] = dict_player
        elif item.position_id == 3:
            dict_tables['playerThree'] = dict_player
        elif item.position_id == 4:  
            dict_tables['playerFour'] = dict_player
    
    return dict_tables

def get_all_tables_by_round(request:Request, page: int, per_page: int, round_id: str, db: Session):  
    
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    
    api_uri = str(settings.api_uri) 
    
    str_from = "FROM events.domino_boletus dbol join events.domino_rounds dron ON dron.id = dbol.round_id " +\
        "join events.domino_tables dtable ON dtable.id = dbol.table_id " +\
        "Where dbol.round_id = '" + round_id + "' "
        
    str_count = "Select count(*) " + str_from
    str_query = "Select dron.round_number, dtable.table_number, dtable.is_smart, dbol.id as boletus_id, " +\
        "dbol.status_id " + str_from 
    
    if page and page > 0 and not per_page:
        raise HTTPException(status_code=404, detail=_(locale, "commun.invalid_param"))
    
    result = get_result_count(page=page, per_page=per_page, str_count=str_count, db=db)
    
    str_query += " ORDER BY dtable.table_number ASC " 
    if page != 0:
        str_query += "LIMIT " + str(per_page) + " OFFSET " + str(page*per_page-per_page)
    
    lst_data_exec = db.execute(str_query)
    
    lst_data = []
    one_status_init = get_one_status_by_name('INITIADED', db=db)
    
    for item in lst_data_exec:
        status_id = '0' if not item.status_id else '0' if item.status_id == one_status_init.id else '1'
        
        dict_inf_pair = get_info_of_boletus_pair(item.boletus_id, api_uri=api_uri, db=db)
        dict_inf_pair['round_number'] = item.round_number
        dict_inf_pair['table_number'] = item.table_number
        dict_inf_pair['table_type'] = 'Inteligente' if item.is_smart else 'Tradicional'
        dict_inf_pair['boletus_id'] = item.boletus_id
        dict_inf_pair['status'] = status_id
        dict_inf_pair['status_partida'] = 'Partido Terminado' if status_id == '1' else 'Partido Jugando'
        lst_data.append(dict_inf_pair)
    
    result.data = lst_data
    return result

def get_info_of_boletus_pair(boletus_id: str, api_uri: str, db: Session):
    
    dict_result = {'pair_one' : {'name': '', 'player_one': '', 'player_two': '', 
                                 'avatar_one': '', 'avatar_two': '', 'elo_one': '', 'elo_two': '',
                                 'positive_point': 0, 'negative_point': 0, 'difference_point': 0,
                                 'is_winner': False},
                   'pair_two' : {'name': '', 'player_one': '', 'player_two': '', 
                                 'avatar_one': '', 'avatar_two': '', 'elo_one': '', 'elo_two': '',
                                 'positive_point': 0, 'negative_point': 0, 'difference_point': 0,
                                 'is_winner': False}}
    
    str_query = "Select dpair.name, pairs_id, dbpair.positive_points, dbpair.negative_points, " +\
        "dbpair.is_winner, sca_one.elo elo_one, sca_two.elo elo_two, pmone.name name_one, pmtwo.name name_two, " +\
        "pmone.photo photo_one, pmtwo.photo photo_two, pmone.id profile_id_one, pmtwo.id profile_id_two " +\
        "from events.domino_boletus_pairs dbpair " +\
        "join events.domino_boletus dbol ON dbol.id = dbpair.boletus_id " +\
        "join events.domino_rounds_pairs dpair ON dpair.id = dbpair.pairs_id " +\
        "join events.domino_rounds_scale sca_one ON sca_one.id = dpair.scale_id_one_player " +\
        "join events.domino_rounds_scale sca_two ON sca_two.id = dpair.scale_id_two_player " +\
        "join enterprise.profile_member pmone ON pmone.id = dpair.one_player_id " +\
        "join enterprise.profile_member pmtwo ON pmtwo.id = dpair.two_player_id " +\
        "where dbpair.boletus_id = '" + boletus_id + "' "
        
    lst_data_exec = db.execute(str_query)
    pair_number = 1
    for item in lst_data_exec:
        name_key = 'pair_one' if pair_number == 1 else 'pair_two'
        dict_result[name_key]['name'] = item.name
        dict_result[name_key]['player_one'] = item.name_one
        dict_result[name_key]['player_two'] = item.name_two
        dict_result[name_key]['avatar_one'] = get_url_avatar(item.profile_id_one, item.photo_one, api_uri=api_uri)
        dict_result[name_key]['avatar_two'] = get_url_avatar(item.profile_id_two, item.photo_two, api_uri=api_uri)
        dict_result[name_key]['elo_one'] = item.elo_one
        dict_result[name_key]['elo_two'] = item.elo_two
        dict_result[name_key]['positive_point'] = int(item.positive_points) if item.positive_points else 0
        dict_result[name_key]['negative_point'] = int(item.negative_points) if item.negative_points else 0
        dict_result[name_key]['difference_point'] = dict_result['pair_one']['positive_point'] - dict_result['pair_one']['negative_point']
        dict_result[name_key]['is_winner'] = item.is_winner
        pair_number += 1
        
    return dict_result

def get_one_round_pair(id: str, db: Session):  
    return db.query(DominoRoundsPairs).filter(DominoRoundsPairs.id == id).first()

def get_one_round_scale(id: str, db: Session):  
    return db.query(DominoRoundsScale).filter(DominoRoundsScale.id == id).first()

def update_info_pairs(pair_win_id: str, pair_lost_id: str,  total_point: int, db: Session):
    
    win_pair = get_one_round_pair(pair_win_id, db=db)
    lost_pair = get_one_round_pair(pair_lost_id, db=db)

    scale_player_win_one = get_one_round_scale(win_pair.scale_id_one_player, db=db) if win_pair.scale_id_one_player else None
    scale_player_win_two = get_one_round_scale(win_pair.scale_id_two_player, db=db) if win_pair.scale_id_two_player else None
    
    scale_player_lost_one = get_one_round_scale(win_pair.scale_id_one_player, db=db) if win_pair.scale_id_one_player else None
    scale_player_lost_two = get_one_round_scale(win_pair.scale_id_two_player, db=db) if win_pair.scale_id_two_player else None
    
    elo_win_pair = scale_player_lost_one.elo if scale_player_lost_one else 0 + scale_player_lost_two.elo if scale_player_lost_two else 0
    elo_lost_pair = scale_player_lost_one.elo if scale_player_lost_one else 0 + scale_player_lost_two.elo if scale_player_lost_two else 0
    
    update_wind_pair(win_pair, scale_player_win_one, scale_player_win_two, elo_win_pair, elo_lost_pair, positive_point=total_point, db=db)
    
    update_lost_pair(lost_pair, scale_player_lost_one, scale_player_lost_two, elo_win_pair, elo_lost_pair, negative_point=total_point, db=db)
    
    return True

def update_wind_pair(win_pair, scale_player_win_one, scale_player_win_two, elo_win_pair, elo_lost_pair, positive_point:int, db: Session):
    
    if scale_player_win_one:
        scale_player_win_one.games_played = scale_player_win_one.games_played + 1 if scale_player_win_one.games_played else 1
        scale_player_win_one.games_won = scale_player_win_one.games_won + 1 if scale_player_win_one.games_won else 1
        scale_player_win_one.games_lost = scale_player_win_one.games_lost if scale_player_win_one.games_lost else 0
        scale_player_win_one.points_positive = scale_player_win_one.points_positive + positive_point if scale_player_win_one.points_positive \
            else positive_point
        scale_player_win_one.points_negative = scale_player_win_one.points_negative + 0 if scale_player_win_one.points_negative \
            else 0
        scale_player_win_one.points_difference = scale_player_win_one.points_positive - scale_player_win_one.points_negative
        
        scale_player_win_one.elo_variable = calculate_new_elo(
            scale_player_win_one.elo, scale_player_win_one.games_played, scale_player_win_one.points_positive, 
            scale_player_win_one.points_negative, True, elo_win_pair, elo_lost_pair)
        
        db.add(scale_player_win_one)
            
    if win_pair.scale_id_two_player:
        scale_player_win_two = get_one_round_scale(win_pair.scale_id_two_player, db=db)
        if scale_player_win_two:
            scale_player_win_two.games_played = scale_player_win_two.games_played + 1 if scale_player_win_two.games_played else 1
            scale_player_win_two.games_won = scale_player_win_two.games_won + 1 if scale_player_win_two.games_won else 1
            scale_player_win_one.games_lost = scale_player_win_two.games_lost if scale_player_win_two.games_lost else 0
            scale_player_win_two.points_positive = scale_player_win_two.points_positive + positive_point if scale_player_win_two.points_positive \
                else positive_point
            scale_player_win_two.points_negative = scale_player_win_two.points_negative + 0 if scale_player_win_two.points_negative \
                else 0
            scale_player_win_two.points_difference = scale_player_win_two.points_positive - scale_player_win_two.points_negative
            scale_player_win_two.elo_variable = calculate_elo(positive_point, scale_player_win_two.elo)
            
            scale_player_win_two.elo_variable = calculate_new_elo(
            scale_player_win_two.elo, scale_player_win_two.games_played, scale_player_win_two.points_positive, 
            scale_player_win_two.points_negative, True, elo_win_pair, elo_lost_pair)
            
            db.add(scale_player_win_two)
    
    try:
        db.commit()
        return TraceLotteryManual
       
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        return False
    
def update_lost_pair(lost_pair, scale_player_lost_one, scale_player_lost_two, elo_win_pair, elo_lost_pair, negative_point:int, db: Session):
    
    if lost_pair.scale_id_one_player:
        scale_player_lost_one = get_one_round_scale(lost_pair.scale_id_one_player, db=db)
        if scale_player_lost_one:
            
            scale_player_lost_one.games_played = scale_player_lost_one.games_played + 1 if scale_player_lost_one.games_played else 1
            scale_player_lost_one.games_lost = scale_player_lost_one.games_lost + 1 if scale_player_lost_one.games_lost else 1
            scale_player_lost_one.games_won = scale_player_lost_one.games_won if scale_player_lost_one.games_won else 0
            
            scale_player_lost_one.points_negative = scale_player_lost_one.points_negative + negative_point if scale_player_lost_one.points_negative \
                else negative_point
            scale_player_lost_one.points_positive = scale_player_lost_one.points_positive + 0 if scale_player_lost_one.points_positive \
                else 0
            scale_player_lost_one.points_difference = scale_player_lost_one.points_positive - scale_player_lost_one.points_negative
            
            scale_player_lost_one.elo_variable = calculate_new_elo(
            scale_player_lost_one.elo, scale_player_lost_one.games_played, scale_player_lost_one.points_positive, 
            scale_player_lost_one.points_negative, True, elo_win_pair, elo_lost_pair)
            
            db.add(scale_player_lost_one)
            
    if lost_pair.scale_id_two_player:
        scale_player_lost_two = get_one_round_scale(lost_pair.scale_id_two_player, db=db)
        if scale_player_lost_two:
            
            scale_player_lost_two.games_played = scale_player_lost_two.games_played + 1 if scale_player_lost_two.games_played else 1
            scale_player_lost_two.games_lost = scale_player_lost_two.games_lost + 1 if scale_player_lost_two.games_lost else 1
            scale_player_lost_two.games_won = scale_player_lost_two.games_won if scale_player_lost_two.games_won else 0
            
            scale_player_lost_two.points_negative = scale_player_lost_two.points_negative + negative_point if scale_player_lost_two.points_negative \
                else negative_point
            scale_player_lost_two.points_positive = scale_player_lost_two.points_positive + 0 if scale_player_lost_two.points_positive \
                else 0
            scale_player_lost_two.points_difference = scale_player_lost_two.points_positive - scale_player_lost_two.points_negative
            
            scale_player_lost_two.elo_variable = calculate_new_elo(
            scale_player_lost_two.elo, scale_player_lost_two.games_played, scale_player_lost_two.points_positive, 
            scale_player_lost_two.points_negative, True, elo_win_pair, elo_lost_pair)
            
            db.add(scale_player_lost_two)

    try:
        db.commit()
        return TraceLotteryManual
       
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        return False
 
def calculate_elo(point: int, elo_actual: float):
    
    elo_actual = float(elo_actual) + point if elo_actual else point
    return elo_actual

def get_values_elo_by_scale(round_id: str, db: Session):  
    
    str_query = "SELECT MAX(elo_variable) elo_max, MIN(elo_variable) elo_min " +\
        "FROM events.domino_rounds_scale Where round_id = '" + round_id + "' "
    
    lst_data = db.execute(str_query)
    elo_max, elo_min = float(0.00), float(0.00)
    for item in lst_data:
        elo_max = item.elo_max
        elo_min = item.elo_min
    
    return elo_max, elo_min

def aperture_new_round(request:Request, round_id:str, round: DominoRoundsAperture, db:Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    # si la ronda no se ha publicado, puede eliminarse y volver a configurar..
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    db_round = get_one_round(round_id=round_id, db=db)
    if not db_round:
        raise HTTPException(status_code=404, detail=_(locale, "round.not_found"))
    
    one_status_created = get_one_status_by_name('CREATED', db=db)
    if not one_status_created:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_found"))
    
    one_status_conf = get_one_status_by_name('CONFIGURATED', db=db)
    if not one_status_conf:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_found"))
    
    if db_round.status.name not in ('CREATED', 'CONFIGURATED'):
        raise HTTPException(status_code=404, detail=_(locale, "round.status_incorrect"))
    
    info_round = get_obj_info_to_aperturate(db_round, db) 
    
    if info_round.amount_players_playing < 8:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.amount_player_incorrect"))
    
    str_query = "SELECT count(tourney_id) FROM events.domino_categories where tourney_id = '" + db_round.tourney.id + "' "
    amount = db.execute(str_query).fetchone()[0]
    if amount == 0:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.category_not_configurated"))
    
    if db_round.is_first:
        # validar todas las categorias estén contempladas entre los elo de los jugadores.
        lst_category = get_lst_categories_of_tourney(tourney_id=db_round.tourney.id, db=db)
        if not verify_category_is_valid(float(db_round.tourney.elo_max), float(db_round.tourney.elo_min), lst_category=lst_category):
            raise HTTPException(status_code=400, detail=_(locale, "tourney.setting_category_incorrect"))
        
        result_init = order_round_to_init(db_round, db=db)
        if not result_init:
            raise HTTPException(status_code=404, detail=_(locale, "tourney.setting_initial_scale_failed"))

    else:
        result_init = order_round_to_play(db_round, db=db)
        if not result_init:
            raise HTTPException(status_code=404, detail=_(locale, "tourney.setting_initial_scale_failed"))
    
    # configure_tables_by_round(db_round.tourney.id, db_round.id, db_round.tourney.modality, db_round.tourney.updated_by, db=db)
    
    db_round.status_id = one_status_conf.id
     
    one_status_init = get_one_status_by_name('INITIADED', db=db)
    if not one_status_init:
        raise HTTPException(status_code=404, detail=_(locale, "status.not_found"))
    
    db_round.tourney.status_id = one_status_init.id
    db_round.tourney.event.status_id = one_status_init.id
    
    db.add(db_round)
    db.add(db_round.tourney)
    db.add(db_round.tourney.event)
    
    db.commit()
    
    # try:
    #     configure_new_rounds(
    #         tourney_id=tourney_id, summary='', db=db, created_by=currentUser['username'], round_number=info_round.round_number,
    #         is_first=info_round.is_first, is_last=info_round.is_last, use_segmentation=round.use_segmentation, 
    #         use_bonus=round.use_bonus, amount_bonus_tables=round.amount_bonus_tables, amount_bonus_points=round.amount_bonus_points,
    #         amount_tables=info_round.amount_tables, amount_categories=info_round.amount_categories, 
    #         amount_players_playing=info_round.amount_players_playing, amount_players_waiting=info_round.amount_players_waiting,
    #         amount_players_pause=info_round.amount_players_pause, amount_players_expelled=info_round.amount_players_expelled)
    #     return result
    
    # except (Exception, SQLAlchemyError, IntegrityError) as e:
    #     raise HTTPException(status_code=404, detail=_(locale, "round.error_started_round"))

    return result

def verify_category_is_valid(elo_max: float, elo_min: float, lst_category: list):
    
    current_elo_max = float(elo_max)
    current_elo_min = float(elo_min)
    
    for item in lst_category:
        if current_elo_max !=  float(item['elo_max']):
            return False
        else:
            current_elo_max = float(item['elo_min']) - 1 
            current_elo_min = float(item['elo_min'])
    
    if current_elo_min != float(elo_min) and current_elo_min < elo_min:
        return False
    
    return True

def order_round_to_init(db_round, db:Session):
    
    if db_round.tourney.lottery_type == "MANUAL":
        # salvar la escala manual
        result_init = configure_manual_lottery(db_round, db=db)
    else:
        result_init = configure_automatic_lottery(db_round, db=db)
            
    if not result_init:
        return False
    
    return True   

def order_round_to_play(db_round, db:Session):
    
    return True  

def order_round_to_end(db_round, db:Session):
    
    return True 