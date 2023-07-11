from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String,Date,DECIMAL, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database.database import Base


class FuelEnum(str, Enum):
    Gasoline = 'Gasoline'
    Diesel = 'Diesel'
    Electric = 'Electric'

    
class TransmissionEnum(str, Enum):
    Manual = 'Manual'
    Automatic = 'Automatic'


class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    vehicles = relationship("DbVehicle", back_populates="owner")
    bookings = relationship("DbBooking", back_populates="user")

class DbVehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    model = Column(String)
    price = Column(DECIMAL(10, 2))
    location = Column(String)
    fuel = Column(SQLAlchemyEnum(FuelEnum))
    transmission = Column(SQLAlchemyEnum(TransmissionEnum))
    seats=Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("DbUser", back_populates="vehicles")
    bookings = relationship("DbBooking", back_populates="vehicle")
    photos = relationship("DbPhoto", back_populates="vehicle")

class DbPhoto(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    photo_path = Column(String)
    vehicle = relationship("DbVehicle", back_populates="photos")

class DbBooking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    vehicle = relationship("DbVehicle", back_populates="bookings")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("DbUser", back_populates="bookings")
    start_date = Column(Date)
    end_date = Column(Date)
