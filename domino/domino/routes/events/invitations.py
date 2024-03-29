from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from domino.app import get_db
from typing import List, Dict
from starlette import status
from domino.auth_bearer import JWTBearer

from domino.schemas.resources.result_object import ResultObject
from domino.schemas.events.invitations import InvitationAccepted, InvitationFilters

from domino.services.events.invitations import generate_all_user, update, get_all_invitations_by_user, get_all_invitations_by_tourney
  
invitation_route = APIRouter(
    tags=["Invitations"],
    dependencies=[Depends(JWTBearer())]   
)

@invitation_route.get("/invitation", response_model=ResultObject, summary="Get All Invitations for user logued.")
def get_all(request:Request, profile_id: str, status_name:str, db: Session = Depends(get_db)):
    return get_all_invitations_by_user(request=request, profile_id=profile_id, status_name=status_name, db=db)

@invitation_route.get("/invitation/tourney/", response_model=Dict, summary="Get All Invitations for tourney.")
def get_for_tourney(
    request:Request, 
    tourney_id: str, 
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    player_name: str = "", 
    db: Session = Depends(get_db)):
    return get_all_invitations_by_tourney(
        request=request, tourney_id=tourney_id, page=page, per_page=per_page, criteria_key=criteria_key, criteria_value=criteria_value, 
        player_name=player_name, db=db)

@invitation_route.post("/invitation", response_model=ResultObject, summary="Generate user invitations")
def generate(request:Request, tourney_id: str, filters_invitation: InvitationFilters, db: Session = Depends(get_db)):
    return generate_all_user(request=request, tourney_id=tourney_id, filters_invitation=filters_invitation, db=db)

@invitation_route.put("/invitation/{id}", response_model=ResultObject, summary="Accept or Rejected Invitation")
def update_invitation(request:Request, id: str, invitation: InvitationAccepted, db: Session = Depends(get_db)):
    return update(request=request, db=db, invitation_id=str(id), invitation=invitation)
