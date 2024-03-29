# Routes user.py

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from domino.app import get_db
from typing import List, Dict
from starlette import status
from domino.auth_bearer import JWTBearer
import uuid

from fastapi.responses import FileResponse
from os import getcwd

from domino.schemas.enterprise.user import UserShema, UserCreate, UserBase, ChagePasswordSchema, UserFollowerBase
from domino.schemas.enterprise.userprofile import DefaultUserProfileBase
from domino.schemas.resources.result_object import ResultObject

from domino.services.enterprise.users import get_all, get_one_by_id, delete, update, change_password, get_one_profile, \
    add_one_followers, remove_one_followers, get_all_followers, get_all_not_followers

from domino.services.enterprise.userprofile import new_generic_default_profile, update_one_default_profile
    
user_route = APIRouter(
    tags=["Users"],
    dependencies=[Depends(JWTBearer())]
)

@user_route.get("/users", response_model=Dict, summary="Get list of Users.")
def get_users(request: Request, page: int = 1, per_page: int = 6, search: str = "", db: Session = Depends(get_db)):
    return get_all(request=request, page=page, per_page=per_page, criteria_value=search, db=db)

@user_route.get("/users/{id}", response_model=ResultObject, summary="Get a User by his ID")
def get_user_by_id(request:Request, id: str, db: Session = Depends(get_db)):
    return get_one_by_id(user_id=id, db=db, request=request)

@user_route.post("/users", response_model=ResultObject, summary="Create a New user")
def create_default_profile(request:Request, defaultusereprofile: DefaultUserProfileBase = Depends(), image: UploadFile = None, db: Session = Depends(get_db)):
    return new_generic_default_profile(request=request, db=db, defaultuserprofile=defaultusereprofile.dict(), avatar=image)

@user_route.put("/users/{id}", response_model=ResultObject, summary="Update Default User Profile for your ID")
def update_default_profile(request:Request, id: str, defaultusereprofile: DefaultUserProfileBase = Depends(), image: UploadFile = None, db: Session = Depends(get_db)):
    return update_one_default_profile(request=request, db=db, id=str(id), defaultuserprofile=defaultusereprofile.dict(), avatar=image)

@user_route.delete("/users/{id}", response_model=ResultObject, summary="Eliminar un Usuario por su ID")
def delete_user(request:Request, id: uuid.UUID, db: Session = Depends(get_db)):
    return delete(request=request, user_id=str(id), db=db)
    
# @user_route.put("/users/{id}", response_model=ResultObject, summary="Update a User by his ID.")
# def update_user(request:Request, id: uuid.UUID, user: UserProfile = Depends(), avatar: UploadFile = None, db: Session = Depends(get_db)):
#     return update_one_profile(request=request, db=db, user_id=str(id), user=user, avatar=avatar)

@user_route.post("/users/password", response_model=ResultObject, summary="Change password to a user.")
def reset_password(
    request: Request,
    password: ChagePasswordSchema,
    db: Session = Depends(get_db)
):
    return change_password(request=request, db=db, password=password)

# @user_route.post("/users/followers", response_model=ResultObject, summary="Add Followers at User")
# def add_followers(request:Request, userfollower: UserFollowerBase, db: Session = Depends(get_db)):
#     return add_one_followers(request=request, db=db, userfollower=userfollower)

# @user_route.delete("/users/followers/{user_name_follower}", response_model=ResultObject, summary="Remove Followers at User")
# def delete_followers(request:Request, user_name_follower: str, db: Session = Depends(get_db)):
#     return remove_one_followers(request=request, db=db, user_follower=user_name_follower)

# @user_route.get("/users/followers/", response_model=Dict, summary="Get list of Followers.")
# def get_followers(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     return get_all_followers(request=request, db=db)

# @user_route.get("/users/not_followers/", response_model=Dict, summary="Get list of followers suggestion.")
# def get_followers_suggestion(
#     request: Request,
#     db: Session = Depends(get_db)
# ):
#     return get_all_not_followers(request=request, db=db)

@user_route.get("/users/{user_id}/{name}", summary="Mostrar la imagen de perfil de un usuario")
def getprofile(user_id: str, file_name: str):
    return FileResponse(getcwd() + "/public/profile/" + user_id + "/" + file_name)