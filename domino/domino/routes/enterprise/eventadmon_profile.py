from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from domino.app import get_db
from starlette import status
from domino.auth_bearer import JWTBearer

from domino.schemas.enterprise.userprofile import EventAdmonProfileCreated, GenericProfileCreated
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.enterprise.userprofile import new_profile_event_admon, get_one_eventadmon_profile_by_id, \
    update_one_event_admon_profile, delete_one_profile, get_all_eventadmon_profile, new_generic_event_admon, \
    update_generic_event_admon_profile, get_generic_eventadmon_profile_by_id
  
eventadmonprofile_route = APIRouter(
    tags=["Profile"],
    dependencies=[Depends(JWTBearer())]   
)

# @eventadmonprofile_route.post("/profile/eventadmon", response_model=ResultObject, summary="Create a Profile of Event Admon")
# def create_eventadmon_profile(
#     request:Request, eventadmonprofile: EventAdmonProfileCreated = Depends(), image: UploadFile = None, db: Session = Depends(get_db)):
#     return new_profile_event_admon(request=request, eventadmonprofile=eventadmonprofile.dict(), file=image, db=db)

# @eventadmonprofile_route.get("/profile/eventadmon/{id}", response_model=ResultObject, summary="Get a Event Admon Profile for your ID.")
# def get_eventadmon_profile(request: Request, id: str, db: Session = Depends(get_db)):
#     return get_one_eventadmon_profile_by_id(request, id=id, db=db)

# @eventadmonprofile_route.delete("/profile/eventadmon/{id}", response_model=ResultObject, summary="Remove Event Admon Profile for your ID")
# def delete_eventadmon_profile(request:Request, id: str, db: Session = Depends(get_db)):
#     return delete_one_profile(request=request, id=str(id), db=db)
    
# @eventadmonprofile_route.put("/profile/eventadmon/{id}", response_model=ResultObject, summary="Update Event Admon Profile for your ID")
# def update_eventadmon_profile(
#     request:Request, id: str, eventadmonprofile: EventAdmonProfileCreated = Depends(), image: UploadFile = None, db: Session = Depends(get_db)):
#     return update_one_event_admon_profile(request=request, db=db, id=str(id), eventadmonprofile=eventadmonprofile.dict(), file=image)


@eventadmonprofile_route.get("/profile/federative/{profile_id}", response_model=ResultData, summary="Obtain a list of Eventy Admon profile")
def get_profile(request: Request, profile_id: str, page: int = 1, per_page: int = 6, search: str = "", db: Session = Depends(get_db)):
    return get_all_eventadmon_profile(request=request, profile_id=profile_id, page=page, per_page=per_page, 
                                      criteria_value=search, db=db)
    
@eventadmonprofile_route.post("/profile/federative/{profile_id}", response_model=ResultObject, summary="Create a Profile of Event Admon")
def create_eventadmon_generic_profile(
    request:Request, profile_id: str, eventadmonprofile: GenericProfileCreated = Depends(), image: UploadFile = None, db: Session = Depends(get_db)):
    return new_generic_event_admon(request=request, profile_id=profile_id, eventadmonprofile=eventadmonprofile.dict(), file=image, db=db)

@eventadmonprofile_route.put("/profile/federative/{id}", response_model=ResultObject, summary="Update Event Admon Profile for your ID")
def update_eventadmon_generic_profile(
    request:Request, id: str, eventadmonprofile: GenericProfileCreated = Depends(), image: UploadFile = None, db: Session = Depends(get_db)):
    return update_generic_event_admon_profile(request=request, db=db, id=str(id), eventadmonprofile=eventadmonprofile.dict(), file=image)

@eventadmonprofile_route.get("/profile/federative/one/{id}", response_model=ResultObject, summary="Get a Event Admon Profile for your ID.")
def get_eventadmon_generic_profile(request: Request, id: str, db: Session = Depends(get_db)):
    return get_generic_eventadmon_profile_by_id(request, id=id, db=db)