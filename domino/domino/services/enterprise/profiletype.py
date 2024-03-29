import math

from fastapi import HTTPException, Request
from unicodedata import name
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.context import CryptContext
from domino.auth_bearer import decodeJWT
from domino.functions_jwt import get_current_user
from domino.app import _

from domino.models.enterprise.userprofile import ProfileType
from domino.schemas.enterprise.profiletype import ProfileTypeSchema, ProfileTypeBase
from domino.schemas.resources.result_object import ResultObject

from domino.services.resources.utils import get_result_count
            
def get_all(request:Request, db: Session):  
    
    result = ResultObject()
    
    currentUser = get_current_user(request)
    
    str_query = "Select id, name, description FROM enterprise.profile_type where by_default is False "
    str_profile = "SELECT DISTINCT pmem.profile_type FROM enterprise.profile_users puse " +\
        "INNER JOIN enterprise.profile_member pmem ON pmem.id = puse.profile_id " +\
        "WHERE profile_type != 'USER' AND username = '"  + currentUser['username'] + "' "
  
    lst_data = db.execute(str_query)
    
    lst_profile = db.execute(str_profile)
    str_profile = ""
    for item_pro in lst_profile:
        str_profile += " " + item_pro['profile_type']
    
    result.data = []    
    for item in lst_data:
        if item['name'] in ('JOURNALIST', 'COACH'):  # no tengo preparada estas clases
            continue
        elif item['name'] in ('PAIR_PLAYER', 'TEAM_PLAYER'):  # de este tipo puede tener varios
            result.data.append({'id': item['id'], 'name' : item['name'], 'description': item['description']})
        else:
            if item['name'] in str_profile:
                continue
            else:
                result.data.append({'id': item['id'], 'name' : item['name'], 'description': item['description']})
    
    return result

def get_one(id: str, db: Session):  
    return db.query(ProfileType).filter(ProfileType.id == id).first()

def get_one_by_name(name: str, db: Session):  
    return db.query(ProfileType).filter(ProfileType.name == name).first()
      
def new(request, db: Session, profiletype: ProfileTypeBase):
    locale = request.headers["accept-language"].split(",")[0].split("-")[0];
    
    result = ResultObject() 
    currentUser = get_current_user(request)
    
    db_pro_type = get_one_by_name(profiletype.name, db=db)
    if db_pro_type:
        raise HTTPException(status_code=404, detail=_(locale, "profiletype.exist_name"))
        
    db_pro_type = ProfileType(name=profiletype.name, description=profiletype.description, created_by=currentUser['username'])
    
    try:
        db.add(db_pro_type)
        db.commit()
        return result
    except (Exception, SQLAlchemyError, IntegrityError) as e:
        print(e)
        msg = _(locale, "profiletype.error_new_status")
        if e.code == 'gkpj':
            field_name = str(e.__dict__['orig']).split('"')[1].split('_')[1]
            if field_name == 'username':
                msg = msg + _(locale, "profiletype.already_exist")
        
        raise HTTPException(status_code=403, detail=msg)