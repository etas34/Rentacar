
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from database.models import DbUser, DbVehicle
from helpers import check_user

from routers.schemas import UserBase
from database.hashing import Hash


def create (db: Session, request: UserBase): 
    new_user= DbUser(
        name = request.name,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update(db: Session,id: int, request: UserBase): 
    check_user(id,db)
    db_user =db.query(DbUser).filter(DbUser.id==id)
    db_user.update({        
        DbUser.name : request.name,
        DbUser.email  : request.email,
        DbUser.password : Hash.bcrypt(request.password)
    })

    db.commit()
    db.refresh(db_user.first())
    return db_user.first()



def get_by_id(db : Session, id):
    return db.query(DbUser).filter(DbUser.id==id).first()



def get_all(db : Session):
    return db.query(DbUser).all()


def get_user_by_username(db: Session, username: str):
    user= db.query(DbUser).filter(DbUser.email==username).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User not found')
    
    return user

def delete(db: Session, id: int):
    check_user(id,db)
    db.query(DbVehicle).filter(DbVehicle.owner_id==id).delete()
    user= db.query(DbUser).filter(DbUser.id==id).first()
    db.delete(user)
    db.commit()
    return 'ok'


def get_vehicles_by_id(db : Session, id : int):
    check_user(id,db)
    return db.query(DbVehicle).filter(DbVehicle.owner_id==id).all()