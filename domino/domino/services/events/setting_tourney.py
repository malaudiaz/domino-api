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

from domino.schemas.resources.result_object import ResultObject
from domino.schemas.events.tourney import SettingTourneyCreated

from domino.services.resources.status import get_one_by_name as get_one_status_by_name, get_one as get_one_status
from domino.services.resources.utils import get_result_count, upfile, create_dir, del_image, get_ext_at_file, remove_dir
from domino.services.enterprise.users import get_one_by_username
from domino.services.enterprise.userprofile import get_one as get_one_profile
from domino.services.events.domino_boletus import created_boletus_for_round

from domino.services.events.domino_table import created_tables_default
from domino.services.events.domino_round import created_round_default, remove_configurate_round, get_last_by_tourney
from domino.services.events.domino_scale import configure_automatic_lottery, update_elo_initial_scale

from domino.services.events.tourney import get_one as get_one_tourney, calculate_amount_tables, \
    get_count_players_by_tourney, get_values_elo_by_tourney, get_lst_categories_of_tourney, get_categories_of_tourney,\
    create_category_by_default, update_amount_player_by_categories
from domino.services.enterprise.auth import get_url_advertising

def get_one_configure_tourney(request:Request, tourney_id: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject()  
    
    api_uri = str(settings.api_uri)
    
    db_tourney = get_one_tourney(tourney_id=tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))

    amount_tables = calculate_amount_tables(tourney_id=tourney_id, modality=db_tourney.modality, db=db) 
    
    if db_tourney.amount_tables != amount_tables:
        db_tourney.amount_tables = amount_tables
        db.add(db_tourney)
        db.commit()
    
    #actualizar la cantidad de jugadores por categorias
    update_amount_player_by_categories(tourney_id, db=db)
    
    elo_max, elo_min = get_values_elo_by_tourney(tourney_id=tourney_id, db=db)
    
    result.data = {
        "tourney_id": tourney_id, "amount_tables": amount_tables,
        'amount_player': get_count_players_by_tourney(tourney_id, db=db),
        "amount_smart_tables": 0 if not db_tourney.amount_smart_tables else db_tourney.amount_smart_tables,
        "use_bonus": 'NO', #if not db_tourney.amount_smart_tables else 'YES' if setting.use_bonus else 'NO',
        "number_points_to_win": 0 if not db_tourney.number_points_to_win else db_tourney.number_points_to_win,
        "time_to_win": 0 if not db_tourney.time_to_win else db_tourney.time_to_win,
        "game_system": 'SUIZO' if not db_tourney.game_system else db_tourney.game_system,
        'lottery_type': 'MANUAL' if not db_tourney.lottery_type else db_tourney.lottery_type,
        'penalties_limit': 0 if not db_tourney.penalties_limit else db_tourney.penalties_limit,
        'points_penalty_yellow': 0 if not db_tourney.points_penalty_yellow else db_tourney.points_penalty_yellow,
        'points_penalty_red': 0 if not db_tourney.points_penalty_red else db_tourney.points_penalty_red,
        'elo_min': elo_min, 'elo_max': elo_max,
        'constant_increase_ELO': 0 if not db_tourney.constant_increase_elo else db_tourney.constant_increase_elo,
        'image': get_url_advertising(tourney_id=tourney_id, file_name=db_tourney.image, api_uri=api_uri),
        'round_ordering_one': '' if not db_tourney.round_ordering_one else db_tourney.round_ordering_one,
        'round_ordering_two': '' if not db_tourney.round_ordering_two else db_tourney.round_ordering_two,
        'round_ordering_three': '' if not db_tourney.round_ordering_three else db_tourney.round_ordering_three,
        'round_ordering_four': '' if not db_tourney.round_ordering_four else db_tourney.round_ordering_four,
        'round_ordering_five': '' if not db_tourney.round_ordering_five else db_tourney.round_ordering_five,
        'event_ordering_one': '' if not db_tourney.event_ordering_one else db_tourney.event_ordering_one,
        'event_ordering_two': '' if not db_tourney.event_ordering_two else db_tourney.event_ordering_two,
        'event_ordering_three': '' if not db_tourney.event_ordering_three else db_tourney.event_ordering_three,
        'event_ordering_four': '' if not db_tourney.event_ordering_four else db_tourney.event_ordering_four,
        'event_ordering_five': '' if not db_tourney.event_ordering_five else db_tourney.event_ordering_five,
        'status_id': db_tourney.status_id,
        'lst_categories': get_lst_categories_of_tourney(tourney_id=tourney_id, db=db),
        'status_name': db_tourney.status.name,
        'status_description': db_tourney.status.description
        }
        
    return result
    

# def close_configure_one_tourney(request, tourney_id: str, db: Session):
#     locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
#     result = ResultObject() 
#     currentUser = get_current_user(request)
    
#     one_status_conf = get_one_status_by_name('CONFIGURATED', db=db)
    
#     str_query = "SELECT count(tourney_id) FROM events.domino_categories where tourney_id = '" + tourney_id + "' "
#     amount = db.execute(str_query).fetchone()[0]
#     if amount == 0:
#         raise HTTPException(status_code=404, detail=_(locale, "tourney.category_not_configurated"))
    
#     db_tourney = get_one_tourney(tourney_id, db=db)
#     if not db_tourney:
#         raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
    
#     try:
#         elo_max, elo_min = get_values_elo_by_tourney(tourney_id=tourney_id, modality=db_tourney.modality, db=db)
        
#         lst_category = get_lst_categories_of_tourney(tourney_id=tourney_id, db=db)
        
#         db_tourney.elo_max = elo_max
#         db_tourney.elo_min = elo_min
#         db.add(db_tourney)
#         db.commit()
#     except:
#         raise HTTPException(status_code=404, detail=_(locale, "tourney.error_at_closed"))
    
#     # validar todas las categorias estén contempladas entre los elo de los jugadores.
#     if not verify_category_is_valid(float(elo_max), float(elo_min), lst_category=lst_category):
#         raise HTTPException(status_code=400, detail=_(locale, "tourney.setting_category_incorrect"))
    
#     # crear las mesas y sus ficheros
#     result_init = configure_domino_tables(
#         db_tourney, db, currentUser['username'], file=None)
#     if not result_init:
#         raise HTTPException(status_code=400, detail=_(locale, "tourney.setting_tables_failed"))
    
#     # crear la primera ronda
#     db_round_ini = configure_new_rounds(db_tourney.id, 'Ronda Nro. 1', db=db, created_by=currentUser['username'],
#                                         round_number=1)
#     if not db_round_ini:
#         raise HTTPException(status_code=400, detail=_(locale, "tourney.setting_rounds_failed"))
    
#     db_tourney.updated_by = currentUser['username']
    
#     if db_tourney.lottery_type  == 'AUTOMATIC':
#         one_status_init = get_one_status_by_name('INITIADED', db=db)
        
#         # si el sorteo es automático, crear el sorteo inicial, y ya iniciar evento y torneo
#         result_init = configure_automatic_lottery(db_tourney, db_round_ini, one_status_init, db=db)
#         if not result_init:
#             raise HTTPException(status_code=404, detail=_(locale, "tourney.setting_initial_scale_failed"))
        
#     else:
#         db_tourney.status_id = one_status_conf.id
    
#     try:
#         db.add(db_tourney)
#         db.commit()
#     except:
#         raise HTTPException(status_code=404, detail=_(locale, "tourney.error_at_closed"))
    
#     return result

def configure_one_tourney(request, tourney_id: str, settingtourney: SettingTourneyCreated, db: Session):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    db_tourney = get_one_tourney(tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))
    
    if db_tourney.status.name == 'FINALIZED':
        raise HTTPException(status_code=404, detail=_(locale, "tourney.tourney_closed"))
    
    if db_tourney.status.name == 'INITIADED':
        raise HTTPException(status_code=404, detail=_(locale, "tourney.tourney_initiaded"))
    
    amount_tables = calculate_amount_tables(db_tourney.id, db_tourney.modality, db=db)
    
    if amount_tables < 2:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.number_player_incorrect"))

    # try:
    amount_smart_tables = int(settingtourney['amount_smart_tables'])
    number_points_to_win = int(settingtourney['number_points_to_win'])
    time_to_win = int(settingtourney['time_to_win'])
    time_to_win = 12 if not time_to_win else time_to_win
    game_system = str(settingtourney['game_system']) if 'game_system' in settingtourney else ''
    game_system = 'SUIZO' if not game_system else game_system
    lottery_type = str(settingtourney['lottery'])
    lottery_type = 'MANUAL' if not lottery_type else lottery_type
    
    penalties_limit = int(settingtourney['limitPenaltyPoints'])
    points_penalty_yellow = int(settingtourney['points_penalty_yellow'])
    points_penalty_red = int(settingtourney['points_penalty_red'])
    
    constant_increase_ELO = float(settingtourney['constant_increase_ELO'])
    
    round_ordering_one = str(settingtourney['round_ordering_one']) if settingtourney['round_ordering_one'] else None
    round_ordering_two = str(settingtourney['round_ordering_two']) if settingtourney['round_ordering_two'] else None
    round_ordering_three = str(settingtourney['round_ordering_three']) if settingtourney['round_ordering_three'] else None
    round_ordering_four = str(settingtourney['round_ordering_four']) if settingtourney['round_ordering_four'] else None
    round_ordering_five = str(settingtourney['round_ordering_five']) if settingtourney['round_ordering_five'] else None
    
    event_ordering_one = str(settingtourney['event_ordering_one']) if settingtourney['event_ordering_one'] else None
    event_ordering_two = str(settingtourney['event_ordering_two']) if settingtourney['event_ordering_two'] else None
    event_ordering_three = str(settingtourney['event_ordering_three']) if settingtourney['event_ordering_three'] else None
    event_ordering_four = str(settingtourney['event_ordering_four']) if settingtourney['event_ordering_four'] else None
    event_ordering_five = str(settingtourney['event_ordering_five']) if settingtourney['event_ordering_five'] else None
    
    # except:
    #     raise HTTPException(status_code=404, detail=_(locale, "tourney.setting_incorrect"))
    if amount_smart_tables > amount_tables:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.smarttable_incorrect"))
    
    if number_points_to_win <= 0:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.numberpoints_towin_incorrect"))
    
    if not round_ordering_one or not round_ordering_two or not round_ordering_three:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.round_ordering_incorrect"))
    
    if not event_ordering_one or not event_ordering_two or not event_ordering_three:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.event_ordering_incorrect"))
    
    db_tourney.updated_by=currentUser['username']
    
    update_initializes_tourney(
        db_tourney, amount_smart_tables, number_points_to_win, time_to_win, game_system, lottery_type, 
        penalties_limit, db, locale, constant_increase_ELO, points_penalty_yellow, points_penalty_red, round_ordering_one,
        round_ordering_two, round_ordering_three, round_ordering_four, round_ordering_five, event_ordering_one,
        event_ordering_two, event_ordering_three, event_ordering_four, event_ordering_five)
    
    return result

def update_initializes_tourney(db_tourney, amount_smart_tables, number_points_to_win, 
                        time_to_win, game_system, lottery_type, penalties_limit, db: Session,
                        locale, constant_increase_ELO=0, points_penalty_yellow=0, points_penalty_red=0, round_ordering_one=None,
                        round_ordering_two=None, round_ordering_three=None, round_ordering_four=None, round_ordering_five=None,
                        event_ordering_one=None, event_ordering_two=None, event_ordering_three=None, event_ordering_four=None,
                        event_ordering_five=None):
    
    divmod_round = divmod(db_tourney.amount_rounds,5)
    
    db_tourney.amount_smart_tables = amount_smart_tables
    db_tourney.amount_rounds = db_tourney.amount_rounds
    db_tourney.use_bonus = False
    db_tourney.amount_bonus_tables = db_tourney.amount_rounds // 4 
    db_tourney.amount_bonus_points = (db_tourney.amount_rounds // 4) * 2
    db_tourney.number_bonus_round = db_tourney.amount_rounds + 1 if db_tourney.amount_rounds <= 9 else 4 if db_tourney.amount_rounds <= 15 else \
        divmod_round[0] if divmod_round[1] == 0 else divmod_round[0] + 1
    db_tourney.number_points_to_win = number_points_to_win
    
    db_tourney.time_to_win = time_to_win
    db_tourney.game_system = game_system
    db_tourney.lottery_type = lottery_type
    db_tourney.penalties_limit = penalties_limit
    
    elo_max, elo_min = get_values_elo_by_tourney(tourney_id=db_tourney.id, db=db)
    
    db_tourney.elo_max = elo_max
    db_tourney.elo_min = elo_min
    
    db_tourney.constant_increase_ELO = constant_increase_ELO
    db_tourney.points_penalty_yellow = points_penalty_yellow
    db_tourney.points_penalty_red = points_penalty_red
    
    db_tourney.round_ordering_one = round_ordering_one if round_ordering_one else "JUEGOS_GANADOS"
    db_tourney.round_ordering_two = round_ordering_two if round_ordering_two else "ELO_ACUMULADO"
    db_tourney.round_ordering_three = round_ordering_three if round_ordering_three else "DIFERENCIA_TANTOS"
    db_tourney.round_ordering_four = round_ordering_four
    db_tourney.round_ordering_five = round_ordering_five
    
    db_tourney.event_ordering_one = event_ordering_one if event_ordering_one else "JUEGOS_GANADOS"
    db_tourney.event_ordering_two = event_ordering_two if event_ordering_two else "BONIFICACION"
    db_tourney.event_ordering_three = event_ordering_three if event_ordering_three else "ELO"
    db_tourney.event_ordering_four = event_ordering_four
    db_tourney.event_ordering_five = event_ordering_five
       
    # crear las mesas y si ya están creadas borrar y volver a crear
    
    db_round_ini = get_last_by_tourney(db_tourney.id, db=db)
    if db_round_ini:
        result_init = remove_configurate_round(db_tourney.id, db_round_ini.id, db=db)
        status_creat = get_one_status_by_name('CREATED', db=db)
        db_round_ini.status_id = status_creat.id
        
    result_init = created_tables_default(db_tourney, db)
    if not result_init:
        raise HTTPException(status_code=400, detail=_(locale, "tourney.setting_tables_failed"))
    
    # crear la primera ronda, si ya existe, no hacer nada.
    if not db_round_ini:
        db_round_ini = created_round_default(db_tourney, 'Ronda Nro. 1', db=db, round_number=1, is_first=True)
        if not db_round_ini:
            raise HTTPException(status_code=400, detail=_(locale, "tourney.setting_rounds_failed"))
    
    # actualizar elos de las categorias si existen
    lst_category = get_categories_of_tourney(tourney_id=db_tourney.id, db=db)
    if lst_category:
        first_category, last_category = None, None
        for item in lst_category:
            if not first_category:
                first_category = item 
            last_category = item
        if first_category and first_category.elo_max != elo_max:
            first_category.elo_max = elo_max 
            db.add(first_category)
            
        if last_category and last_category.elo_min != elo_min:
            last_category.elo_min = elo_min 
            db.add(last_category)
    else:
        create_category_by_default(db_tourney.id, elo_max, elo_min, amount_players=0, db=db)
    
    #pasar todos los jugadores que estén en estado jugando o en espera a confirmados para que vuelva a empezar la distribución.
    str_update_player = 'UPDATE '    
    # try:
    db.add(db_tourney)
    db.commit()
    return True
       
    # except (Exception, SQLAlchemyError, IntegrityError) as e:
    #     return False