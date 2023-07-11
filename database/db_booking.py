
from datetime import date,timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database.models import DbBooking
from database import db_user, db_vehicle
from helpers import check_booking, check_user, check_vehicle
from routers.schemas import BookingBase
from sqlalchemy.sql import or_, and_
from sqlalchemy.exc import IntegrityError


def create_booking (db: Session, request: BookingBase): 
    vehicle = db_vehicle.get_by_id(db, request.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    user = db_user.get_by_id(db, request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

     # Check if the vehicle is already booked during the specified time
    if (request.start_date> request.end_date): 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start Date must be before than End Date")
    


    conflicting_booking = db.query(DbBooking). \
    filter(
        and_(DbBooking.vehicle_id == request.vehicle_id,
            or_(and_(request.start_date>=DbBooking.start_date, request.start_date <= DbBooking.end_date),
                and_(request.end_date>=DbBooking.start_date, request.end_date <= DbBooking.end_date),
                and_(request.start_date<=DbBooking.start_date, request.end_date >= DbBooking.end_date)))
    ).first()
    if conflicting_booking:        
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vehicle is not available during the specified time")
    
  

    new_booking= DbBooking(
        vehicle_id = request.vehicle_id,
        user_id = request.user_id,
        start_date = request.start_date,
        end_date = request.end_date
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


def get_by_id(db : Session, booking_id):
    return db.query(DbBooking).filter(DbBooking.id==booking_id).first()



def get_all(db : Session):
    return db.query(DbBooking).all()

def update(booking_id:int, db: Session, request: BookingBase):
    check_booking(booking_id,db)
    check_vehicle(request.vehicle_id,db)
    check_user(request.user_id,db)

    # Start a transaction
    
    try:
        # Delete the existing booking
        db.query(DbBooking).filter(DbBooking.id == booking_id).delete()

        # Check if the start date is before the end date
        if request.start_date > request.end_date: 
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start Date must be before than End Date")

        # Check if the vehicle is already booked during the specified time
        conflicting_booking = db.query(DbBooking). \
            filter(
                and_(
                    DbBooking.vehicle_id == request.vehicle_id,
                    or_(
                        and_(
                            request.start_date >= DbBooking.start_date,
                            request.start_date <= DbBooking.end_date
                        ),
                        and_(
                            request.end_date >= DbBooking.start_date,
                            request.end_date <= DbBooking.end_date
                        ),
                        and_(
                            request.start_date <= DbBooking.start_date,
                            request.end_date >= DbBooking.end_date
                        )
                    )
                )
            ).first()
        if conflicting_booking:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vehicle is not available during the specified time")

        # Create the new booking
        new_booking = DbBooking(
            vehicle_id = request.vehicle_id,
            user_id = request.user_id,
            start_date = request.start_date,
            end_date = request.end_date
        )
        db.add(new_booking)
    except IntegrityError:
        # If there is a conflict, rollback the transaction and raise an exception
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vehicle is not available during the specified time")

    else:
        db.commit()
        db.refresh(new_booking)
    return new_booking



def delete(db : Session, id : int):
    check_booking(id,db)
    booking= db.query(DbBooking).filter(DbBooking.id==id).first()
    db.delete(booking)
    db.commit()
    return 'ok'
