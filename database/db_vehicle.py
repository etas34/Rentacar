
from datetime import date
from typing import List
from fastapi import HTTPException, UploadFile, File,status

from sqlalchemy.sql import and_, or_, not_
from sqlalchemy.orm import Session
from database.models import DbBooking, DbPhoto, DbUser, DbVehicle
from routers.schemas import VehicleBase
from helpers import check_user, check_vehicle
from typing import Optional


def create (db: Session, request: VehicleBase, current_user_id:int): 

    
    new_vehicle= DbVehicle(
        brand = request.brand,
        model = request.model,
        price = request.price,
        location = request.location,
        fuel = request.fuel,
        transmission = request.transmission,
        seats = request.seats,
        owner_id = current_user_id
    )

    db.add(new_vehicle)
    db.flush()
    
    for photo in request.photos :

        new_photo= DbPhoto(
        vehicle_id= new_vehicle.id, 
        photo_path = photo    
        )
        db.add(new_photo)

    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle



def update (db: Session, request: VehicleBase, id: int): 
    check_vehicle(id,db)

    db_vehicle= db.query(DbVehicle).filter(DbVehicle.id==id)

    db_vehicle.update({
    DbVehicle.brand : request.brand,
    DbVehicle.model : request.model,
    DbVehicle.price : request.price,
    DbVehicle.location : request.location,
    DbVehicle.fuel : request.fuel,
    DbVehicle.transmission : request.transmission,
    DbVehicle.seats : request.seats,
    DbVehicle.owner_id : request.owner_id

    })
    
    db.commit()
    db.refresh(db_vehicle.first())
    return db_vehicle.first()

def get_all(db : Session):
    return db.query(DbVehicle).all()

def get_available_vehicles(
    db: Session,
    start_date: date,
    end_date: date,
    location: Optional[str] = None,
    seats: Optional[int] = None,
    fuel: Optional[List[str]] = None,
    transmission: Optional[List[str]] = None
):
    query = db.query(DbVehicle)
    if start_date is not None and end_date is not None:
        subquery = db.query(DbBooking.vehicle_id).filter(
            or_(
                and_(start_date >= DbBooking.start_date, start_date <= DbBooking.end_date),
                and_(end_date >= DbBooking.start_date, end_date <= DbBooking.end_date),
                and_(start_date <= DbBooking.start_date, end_date >= DbBooking.end_date)
            )
        ).subquery()

        query = query.filter(not_(DbVehicle.id.in_(subquery)))

    if fuel:
        query = query.filter(DbVehicle.fuel.in_(fuel))
    if transmission:
        query = query.filter(DbVehicle.transmission.in_(transmission))
    if seats:
        query = query.filter(DbVehicle.seats==seats)
    if location:
        query = query.filter(DbVehicle.location.contains(location))

    vehicles = query.all()

    return vehicles


def get_by_id(db : Session, id : int):
    check_vehicle(id,db)
    return db.query(DbVehicle).filter(DbVehicle.id==id).first()




def delete(db : Session, id : int):
    check_vehicle(id,db)
    vehicle= db.query(DbVehicle).filter(DbVehicle.id==id).first()
    db.delete(vehicle)
    db.commit()
    return 'ok'
