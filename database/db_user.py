
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from database.hashing import Hash
from helpers import check_user
from database.models import DbBooking, DbUser, DbVehicle

from routers.schemas import UserBase


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



def get_bookings_by_user_id(db : Session, id : int):

    check_user(id, db)

    # Perform the join between DbBooking, DbVehicle, and DbUser tables
    bookings = db.query(DbBooking). \
        join(DbVehicle, DbBooking.vehicle_id == DbVehicle.id). \
        join(DbUser, DbVehicle.owner_id == DbUser.id). \
        filter(DbUser.id == id). \
        all()

    return bookings