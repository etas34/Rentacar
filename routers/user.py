from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database.database import get_db
from database  import db_user

from routers.schemas import BookingDisplay, UserBase, UserDisplay, VehicleDisplay


router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.post('/', response_model=UserDisplay)
def create_user(request : UserBase, db: Session = Depends(get_db)):
    return db_user.create(db, request)
                


@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    return db_user.get_by_id(db, id)

@router.get("/{id}/vehicles", response_model=List[VehicleDisplay])
def get_user_vehicles(id: int, db: Session = Depends(get_db)):
    return db_user.get_vehicles_by_id(db, id)


@router.get("/{id}/bookings", response_model=List[BookingDisplay])
def get_user_bookings(id: int, db: Session = Depends(get_db)):
    return db_user.get_bookings_by_user_id(db, id)




@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all(db)

@router.put('/{id}', response_model=UserDisplay)
def update_user(id: int, request: UserBase, db : Session=Depends(get_db)):
    return db_user.update(db, id, request)


@router.delete('/{id}')
def delete_user(id: int, db : Session=Depends(get_db)):
    return db_user.delete(db, id)
