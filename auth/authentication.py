from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from database.database import get_db
from database.hashing import Hash
from database.models import DbUser
from auth.oauth2 import create_access_token


router=APIRouter(
    tags=['Authentication']
)

@router.post('/token')
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    user= db.query(DbUser).filter(DbUser.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
    if not Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')
    
    access_token= create_access_token(data={'username': user.email})

    return {
        'access_token'  : access_token,
        'token_type'    : 'Bearer',
        'user_id'       : user.id,
        'user_name'     : user.email 
    }
