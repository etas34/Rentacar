from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from database.database import get_db
from database.db_booking import create_booking, get_by_id, get_all, update, delete

from routers.schemas import BookingBase, BookingDisplay


router = APIRouter(
    prefix='/booking',    tags=['Booking']
)


@router.post('/', response_model=BookingDisplay)
def create(request: BookingBase, db: Session = Depends(get_db)):
    return create_booking(db, request)


@router.get("/{booking_id}", response_model=BookingDisplay)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    return get_by_id(db, booking_id)


@router.get("/", response_model=List[BookingDisplay])
def get_all_bookings(db: Session = Depends(get_db)):
    return get_all(db)


@router.put('/{booking_id}', response_model=BookingDisplay)
def update_booking(booking_id: int, request: BookingBase, db: Session = Depends(get_db)):
    return update(booking_id, db, request)


@router.delete('/{id}')
def delete_booking(id: int,  db: Session = Depends(get_db)):
    return delete(db, id)
