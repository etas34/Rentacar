
import shutil
from typing import List
from fastapi import HTTPException, UploadFile, File,status
from sqlalchemy.orm import Session
from database.models import DbPhoto, DbUser, DbVehicle
from routers.schemas import VehicleBase
import datetime
from helpers import check_photo, check_user, check_vehicle
import os

def create(photo: UploadFile = File(...)):    
    
        
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([suffix, photo.filename])
    save_path = f"images/{filename}"  # Adjust the path or storage mechanism as needed

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    db_photo = DbPhoto(photo_path=save_path)

    return db_photo


def update(photo_id: int,db: Session,  photo: UploadFile = File(...)):
    check_photo(photo_id,db)
    db_photo = db.query(DbPhoto).filter(DbPhoto.id == photo_id).first()
 
    if db_photo.photo_path:
        # Delete the existing photo file
        if os.path.exists(db_photo.photo_path):
            os.remove(db_photo.photo_path)

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    filename = "_".join([suffix, photo.filename])
    save_path = f"images/{filename}"  # Adjust the path or storage mechanism as needed

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    db_photo.photo_path = save_path
    db.commit()
    db.refresh(db_photo)

    return db_photo

def delete(photo_id: int,db: Session):
    check_photo(photo_id,db)
    db_photo = db.query(DbPhoto).filter(DbPhoto.id == photo_id)
 
    if db_photo.first().photo_path:
        # Delete the existing photo file
        if os.path.exists(db_photo.first().photo_path):
            os.remove(db_photo.first().photo_path)

    db_photo.delete()
    db.commit()

    return 'ok'
