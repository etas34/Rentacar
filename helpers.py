from sqlalchemy.orm import Session
from fastapi import HTTPException

from database.models import DbBooking, DbPhoto, DbUser, DbVehicle

def check_user(user_id: int, db: Session) -> bool:
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return True

def check_vehicle(vehicle_id: int, db: Session) -> bool:
    vehicle = db.query(DbVehicle).filter(DbVehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return True

def check_photo(photo_id: int, db: Session) -> bool:
    photo = db.query(DbPhoto).filter(DbPhoto.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return True


def check_booking(booking_id: int, db: Session) -> bool:
    booking = db.query(DbBooking).filter(DbBooking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return True