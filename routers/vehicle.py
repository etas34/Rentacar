from datetime import date
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query,UploadFile,File, Depends
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from database.database import get_db
from database.db_vehicle import create, update, get_all,get_by_id,delete,get_available_vehicles

from routers.schemas import UserAuth, VehicleBase, VehicleDisplay


router = APIRouter(
    prefix='/vehicle',
    tags=['Vehicle']
)

@router.post('/', response_model=VehicleDisplay)
def create_vehicle(request : VehicleBase, db: Session = Depends(get_db), current_user : UserAuth = Depends(get_current_user)):
    return create(db, request, current_user.id)
                
                

@router.put('/{id}', response_model=VehicleDisplay)
def update_vehicle(id:int, request : VehicleBase, db: Session = Depends(get_db)):
    return update(db, request, id)
                

@router.get('/',response_model=list[VehicleDisplay])
def get_all_vehicles(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    location: Optional[str] = Query(None),
    seats: Optional[int] = Query(None),
    fuel: Optional[List[str]] = Query(None),
    transmission: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    if start_date is None and end_date is None and fuel is None and transmission is None and seats is None and location is None:
        return get_all(db)
    elif start_date is not None and end_date is None:
        raise HTTPException(status_code=409, detail='You need to send both start date and end date or none of them')
    elif start_date is  None and end_date is not None:
        raise HTTPException(status_code=409, detail='You need to send both start date and end date or none of them')
    else:
        return get_available_vehicles(db, start_date, end_date,location,seats, fuel, transmission)



@router.get('/{id}',response_model=VehicleDisplay)
def get_vehicle_by_id(id : int, db: Session = Depends(get_db)):
    return get_by_id(db, id)

@router.delete('/{id}')
def delete_vehicle(id:int,  db: Session = Depends(get_db)):
    return delete(db, id)
                