from typing import List
from fastapi import APIRouter,UploadFile,File, Depends
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from database.database import get_db
from database.db_photo import create, update, delete

from routers.schemas import PhotoDisplay, UserAuth, VehicleBase, VehicleDisplay


router = APIRouter(
    prefix='/photo_vehicle',
    tags=['Photo of Vehicle'],
    dependencies=[Depends(get_current_user)]
)


@router.post('/')
def upload_photos(photos: UploadFile = File(...)):
    return create(photos)


@router.put('/{id}')
def update_photo( photo_id: int,  db: Session = Depends(get_db), photo: UploadFile = File(...)):
    return update(photo_id, db, photo)



@router.delete('/{id}')
def delete_photo(id:int,  db: Session = Depends(get_db)):
    return delete(id,db)
                

