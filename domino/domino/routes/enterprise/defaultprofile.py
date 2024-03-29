from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from domino.app import get_db
from starlette import status
from domino.auth_bearer import JWTBearer

from domino.schemas.enterprise.userprofile import DefaultUserProfileBase
from domino.schemas.resources.result_object import ResultObject, ResultData

from domino.services.enterprise.userprofile import get_one_default_user_profile, \
    update_one_default_profile, delete_one_default_profile, get_all_profile_by_user_profile_id, get_all_default_profile

defaultprofile_route = APIRouter(
    tags=["Profile"],
    dependencies=[Depends(JWTBearer())]   
)

@defaultprofile_route.get("/profile/default/", response_model=ResultData, summary="Obtain a list of Default profile")
def get_profile(
    request: Request,
    profile_id: str,
    page: int = 1, 
    per_page: int = 6, 
    criteria_key: str = "",
    criteria_value: str = "",
    db: Session = Depends(get_db)
):
    return get_all_default_profile(request=request, profile_id=profile_id, page=page, per_page=per_page, 
                                   criteria_key=criteria_key, criteria_value=criteria_value, db=db)
    
@defaultprofile_route.get("/profile/default/{id}", response_model=ResultObject, summary="Get a Default User Profile for your ID.")
def get_default_profile(request: Request, id: str, db: Session = Depends(get_db)):
    return get_one_default_user_profile(request, id=id, db=db)

@defaultprofile_route.delete("/profile/default/{id}", response_model=ResultObject, summary="Remove Default User Profile for your ID")
def delete_default_profile(request:Request, id: str, db: Session = Depends(get_db)):
    return delete_one_default_profile(request=request, id=str(id), db=db)
    
@defaultprofile_route.put("/profile/default/{id}", response_model=ResultObject, summary="Update Default User Profile for your ID")
def update_default_profile(request:Request, id: str, defaultusereprofile: DefaultUserProfileBase = Depends(), image: UploadFile = None, db: Session = Depends(get_db)):
    return update_one_default_profile(request=request, db=db, id=str(id), defaultuserprofile=defaultusereprofile.dict(), avatar=image)

@defaultprofile_route.get("/profile/commun/{id}", response_model=ResultObject, summary="Obtener info de perfiles de usuarios")
def get_all_profile_type_by_user(request:Request, id: str, db: Session = Depends(get_db)):
    return get_all_profile_by_user_profile_id(request=request, db=db, profile_id=str(id))



# @defaultprofile_route.put("/users/{id}", response_model=ResultObject, summary="Update a User by his ID.")
# def update_user(request:Request, id: uuid.UUID, user: UserProfile = Depends(), avatar: UploadFile = None, db: Session = Depends(get_db)):
#     return update_one_profile(request=request, db=db, user_id=str(id), user=user, avatar=avatar)

# @defaultprofile_route.get("/profile/{id}", response_model=ResultObject, summary="Get Profile a User by his ID")
# def get_profile(
#     request: Request,
#     id: str, 
#     db: Session = Depends(get_db)
# ):
#     return get_one_profile(request, user_id=id, db=db)


# @auth_routes.post("/register", response_model=ResultObject, tags=["Autentificación"], summary="Register a user on the platform")
# def create_user(request: Request, user: UserCreate = Depends(), avatar: UploadFile = None, db: Session = Depends(get_db)):
#     return new_user(request=request, user=user, db=db, avatar=avatar)