from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from domino.app import get_db
from typing import List, Dict
from starlette import status
from domino.auth_bearer import JWTBearer
from fastapi.responses import FileResponse, JSONResponse
from os import getcwd, remove
from typing import Optional

from domino.schemas.events.tourney import SettingTourneyCreated, DominoCategoryCreated
from domino.schemas.resources.result_object import ResultObject

from domino.services.events.domino_table import get_all, delete, update
from domino.services.events.setting_tourney import get_one_configure_tourney, configure_one_tourney
from domino.services.events.tourney import save_image_tourney, insert_categories_tourney, delete_categories_tourney, get_all_categories_tourney
from domino.services.events.player import get_all_players_by_category
  
settingtourney_route = APIRouter(
    tags=["SettingTourney"],
    dependencies=[Depends(JWTBearer())]   
)

@settingtourney_route.get("/tourney/setting/configure_tables", response_model=Dict, summary="Obtain a list of Domino Tables of Tourney.")
def get_dominotables(
    request: Request,
    profile_id: str,
    tourney_id: str,
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(request=request, profile_id=profile_id, tourney_id=tourney_id, page=page, per_page=per_page, 
                   criteria_key=criteria_key, criteria_value=criteria_value, db=db)
    
@settingtourney_route.put("/tourney/setting/configure_tables/{id}", response_model=ResultObject, summary="Update of Domino Tables by id")
def update_dominotables(request:Request, id: str, image: UploadFile = None, db: Session = Depends(get_db)):
    return update(request=request, db=db, id=str(id), file=image)

@settingtourney_route.delete("/tourney/setting/configure_tables/{id}", response_model=ResultObject, summary="Deactivate a Domino Table by its ID.")
def delete_dominotable(request:Request, id: str, db: Session = Depends(get_db)):
    return delete(request=request, table_id=str(id), db=db)

@settingtourney_route.get("/tourney/setting/{tourney_id}", response_model=Dict, summary="Get Configure Tourney..")
def get_configure_tourney(request:Request, tourney_id: str, db: Session = Depends(get_db)):
    return get_one_configure_tourney(request=request, tourney_id=tourney_id, db=db)

@settingtourney_route.post("/tourney/setting/{id}", response_model=ResultObject, summary="Configure Tourney..")
def configure_tourney(request:Request, id: str, settingtourney: SettingTourneyCreated, db: Session = Depends(get_db)):
    return configure_one_tourney(request=request, tourney_id=id, settingtourney=settingtourney, db=db)  

@settingtourney_route.post("/tourney/setting/images/{id}", response_model=ResultObject, summary="Configure Image of Tourney..")
def configure_setting_image(request:Request, id: str, image: UploadFile = None, db: Session = Depends(get_db)):
    return save_image_tourney(request=request, tourney_id=id, file=image, db=db)

# @settingtourney_route.post("/tourney/setting/categories/{id}", response_model=ResultObject, summary="Configure categories of Tourney..")
# def configure_setting_categories(request:Request, id: str, lst_categories: List[DominoCategoryCreated], db: Session = Depends(get_db)):
#     return configure_categories_tourney(request=request, tourney_id=id, lst_categories=lst_categories, db=db)

@settingtourney_route.post("/tourney/setting/categories/{id}", response_model=ResultObject, summary="Configure news categories of Tourney..")
def created_setting_categories(request:Request, id: str, categories: DominoCategoryCreated, db: Session = Depends(get_db)):
    return insert_categories_tourney(request=request, tourney_id=id, categories=categories, db=db)

@settingtourney_route.delete("/tourney/setting/categories/{id}", response_model=ResultObject, summary="Remove categories of Tourney..")
def delete_setting_categories(request:Request, id: str, db: Session = Depends(get_db)):
    return delete_categories_tourney(request=request, category_id=id, db=db)

@settingtourney_route.get("/tourney/setting/categories/{id}", response_model=Dict, summary="Get categories of Tourney..")
def get_categories_tourney(request:Request, id: str, db: Session = Depends(get_db)):
    return get_all_categories_tourney(request=request, tourney_id=id, db=db)

@settingtourney_route.get("/tourney/setting/categories/player/{id}", response_model=Dict, summary="Get players by categories of Tourney..")
def get_players_by_categories(
    request:Request, 
    id: str, 
    page: int = 1, 
    per_page: int = 6,
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)):
    return get_all_players_by_category(request=request, page=page, per_page=per_page, category_id=id, 
                                       criteria_key=criteria_key, criteria_value=criteria_value, db=db)
    
@settingtourney_route.get("/tourney/setting/nocategories/player/{id}", response_model=Dict, summary="Get players by categories of Tourney..")
def get_players_by_no_categories(
    request:Request, 
    id: str, 
    page: int = 1, 
    per_page: int = 6,
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)):
    return get_all_players_by_category(request=request, page=page, per_page=per_page, category_id='', 
                                       criteria_key=criteria_key, criteria_value=criteria_value, db=db, tourney_id=id)
