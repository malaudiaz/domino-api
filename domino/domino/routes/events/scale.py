from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from domino.app import get_db
from typing import List, Dict
from starlette import status
from domino.auth_bearer import JWTBearer

from domino.schemas.events.domino_rounds import DominoScaleCreated
from domino.schemas.resources.result_object import ResultObject

from domino.services.events.domino_scale import new

dominoscale_route = APIRouter(
    tags=["Rounds"],
    dependencies=[Depends(JWTBearer())]   
)

# @dominoscale_route.get("/tourney/", response_model=Dict, summary="Obtain a list of Tourney.")
# def get_tourney(
#     request: Request,
#     page: int = 1, 
#     per_page: int = 6, 
#     criteria_key: str = "",
#     criteria_value: str = "",
#     db: Session = Depends(get_db)
# ):
#     return get_all(request=request, page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)


@dominoscale_route.post("/domino/scale/initial", response_model=ResultObject, summary="Create Initial Scale..")
def create_initial_scale(request:Request, tourney_id: str, dominoscale: List[DominoScaleCreated], db: Session = Depends(get_db)):
    return new(request=request, tourney_id=tourney_id, dominoscale=dominoscale, db=db)

