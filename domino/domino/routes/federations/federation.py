# Routes federation.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from domino.app import get_db
from typing import List, Dict

from starlette import status
from domino.auth_bearer import JWTBearer

from domino.schemas.federations.federations import FederationsBase
from domino.schemas.resources.result_object import ResultObject

from domino.services.federations.federations import new, update, delete, get_all, get_one_by_id, get_all_list
  
federation_route = APIRouter(
    tags=["Nomenclators"],  # tags=["Countries"],
    dependencies=[Depends(JWTBearer())]   
)

@federation_route.get("/federation", response_model=Dict, summary="Obtain a list of Federations.")
def get_federations(
    request: Request,
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all(
        request=request, page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, db=db)

@federation_route.get("/federation/all/", response_model=Dict, summary="Obtain a list of Federations.")
def get_federations_all(request: Request, db: Session = Depends(get_db)):
    return get_all_list(request=request, db=db)
        
@federation_route.post("/federation", response_model=ResultObject, summary="Create new Federation")
def create_federation(request:Request, federation: FederationsBase, db: Session = Depends(get_db)):
    return new(request=request, federation=federation, db=db)

@federation_route.get("/federation/one/{id}", response_model=ResultObject, summary="Get a Federation for your ID.")
def get_federation_by_id(request:Request, id: int, db: Session = Depends(get_db)):
    return get_one_by_id(request, federation_id=id, db=db)

@federation_route.delete("/federation/{id}", response_model=ResultObject, summary="Remove Federation for your ID")
def delete_federation(request:Request, id: int, db: Session = Depends(get_db)):
    return delete(request=request, federation_id=str(id), db=db)
    
@federation_route.put("/federation/{id}", response_model=ResultObject, summary="Update Federation for your ID")
def update_federation(request:Request, id: int, federation: FederationsBase, db: Session = Depends(get_db)):
    return update(request=request, db=db, federation_id=str(id), federation=federation)