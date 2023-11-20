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

from domino.models.events.domino_round import DominoRounds, DominoRoundsPairs
from domino.models.events.tourney import SettingTourney

from domino.schemas.events.events import EventBase, EventSchema
from domino.schemas.resources.result_object import ResultObject

from domino.services.resources.status import get_one_by_name as get_one_status_by_name, get_one as get_one_status
from domino.services.resources.utils import get_result_count, upfile, create_dir, del_image, get_ext_at_file, remove_dir
from domino.services.enterprise.users import get_one_by_username
from domino.services.enterprise.userprofile import get_one as get_one_profile
from domino.services.events.domino_boletus import created_boletus_for_round

from domino.services.events.tourney import get_one as get_one_tourney, get_setting_tourney, calculate_amount_tables, \
    get_count_players_by_tourney
from domino.services.events.player import get_values_elo_by_tourney
from domino.services.enterprise.auth import get_url_advertising

def get_one_configure_tourney(request:Request, tourney_id: str, db: Session):  
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject()  
    
    api_uri = str(settings.api_uri)
    
    db_tourney = get_one_tourney(tourney_id=tourney_id, db=db)
    if not db_tourney:
        raise HTTPException(status_code=404, detail=_(locale, "tourney.not_found"))

    setting = get_setting_tourney(tourney_id, db=db)
    
    amount_tables = calculate_amount_tables(tourney_id=tourney_id, modality=db_tourney.modality, db=db) if not setting else setting.amount_tables
    
    elo_max, elo_min = get_values_elo_by_tourney(tourney_id=tourney_id, modality=db_tourney.modality, db=db)
    
    result.data = {
        "tourney_id": tourney_id, "amount_tables": amount_tables,
        'amount_player': get_count_players_by_tourney(tourney_id, db_tourney.modality, db=db),
        "amount_smart_tables": 0 if not setting else setting.amount_smart_tables,
        "amount_rounds": 0 if not setting else setting.amount_rounds,
        "use_bonus": 'NO' if not setting else 'YES' if setting.use_bonus else 'NO',
        "amount_bonus_tables": 0 if not setting else setting.amount_bonus_tables,
        "amount_bonus_points": 0 if not setting else setting.amount_bonus_points,
        "number_bonus_round": 0 if not setting else setting.number_bonus_round,
        "number_points_to_win": 0 if not setting else setting.number_points_to_win,
        "time_to_win": 0 if not setting else setting.time_to_win,
        "game_system": '' if not setting else setting.game_system,
        'lottery_type': '' if not setting else setting.lottery_type,
        'penalties_limit': 0 if not setting else setting.penalties_limit,
        'elo_min': elo_min, 'elo_max': elo_max,
        'image': get_url_advertising(tourney_id=tourney_id, file_name=setting.image if setting else None, api_uri=api_uri),
        'status_id': db_tourney.status_id,
        'lst_categories': get_lst_categories_of_tourney(tourney_id=tourney_id, db=db),
        'status_name': db_tourney.status.name,
        'status_description': db_tourney.status.description
        }
    
    return result
    
def get_lst_categories_of_tourney(tourney_id: str, db: Session):
    
    lst_categories = []
    
    str_query = "SELECT id, category_number, position_number, elo_min, elo_max " +\
        "FROM events.domino_categories WHERE tourney_id = '" + tourney_id + "' "
        
    lst_all_category = db.execute(str_query).fetchall()
    for item in lst_all_category:
        lst_categories.append({'category_number': item.category_number,
                              'position_number': item.position_number,
                              'elo_min': item.elo_min, 'elo_max': item.elo_max})
    return lst_categories

