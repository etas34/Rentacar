from datetime import date
from enum import Enum
from fastapi import UploadFile
from pydantic import BaseModel
from typing import List

class FuelEnum(str, Enum):
    Gasoline = 'Gasoline'
    Diesel = 'Diesel'
    Electric = 'Electric'

    
class TransmissionEnum(str, Enum):
    Manual = 'Manual'
    Automatic = 'Automatic'


class UserBase(BaseModel):
    name : str
    email : str
    password : str


class UserDisplay(BaseModel):
    id: int
    name : str
    email : str
    class Config():
        orm_mode= True
    

class VehicleBase(BaseModel):
    brand : str
    model : str
    price : int
    location : str
    fuel : FuelEnum
    transmission : TransmissionEnum
    seats : int
    photos: List[str]


class UserAuth(BaseModel):
    id : int
    name : str
    email : str
    class Config():
        orm_mode= True

class BookingForVehicle(BaseModel):
    start_date: date
    end_date: date
    class Config():
        orm_mode= True

# for vehicle display
class User(BaseModel):
    name : str
    class Config():
        orm_mode= True



class PhotoDisplay(BaseModel):
    id : int
    photo_path : str
    class Config():
        orm_mode= True


class VehicleDisplay(BaseModel):
    id : int
    brand : str
    model : str
    price : float
    owner : User
    location : str
    transmission : str
    fuel : str
    seats : int
    photos : List[PhotoDisplay]
    bookings : List[BookingForVehicle]
    class Config():
        orm_mode= True

class BookingBase(BaseModel):
    user_id : int
    vehicle_id : int
    start_date: date
    end_date: date

# display for booking
class VehicleDisplay_ForBooking(BaseModel):
    brand : str
    model : str
    class Config():
        orm_mode= True

    
class BookingDisplay(BaseModel):
    user : User
    vehicle : VehicleDisplay_ForBooking
    start_date: date
    end_date: date
    class Config():
        orm_mode= True

class PhotoDisplay(BaseModel):
    id : int
    path : str
    class Config():
        orm_mode= True
