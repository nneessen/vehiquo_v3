from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models import vehicles as models
from app.schemas import vehicles as schemas


def get_vehicle_by_id(db: Session, vehicle_id: int) -> Optional[models.Vehicle]:
    """
    Get a vehicle by ID
    @param db: SQLAlchemy database session
    @param vehicle_id: ID of the vehicle to get
    @return: The vehicle with the given ID
    """
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()


def get_vehicles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Vehicle]:
    """
    Get all vehicles
    @param db: SQLAlchemy database session
    @param skip: Number of vehicles to skip
    @param limit: Maximum number of vehicles to return
    @return: A list of vehicles
    """
    return db.query(models.Vehicle).offset(skip).limit(limit).all()


def create_vehicle(db: Session, vehicle: schemas.VehicleAdd) -> models.Vehicle:
    """
    Create a new vehicle
    @param db: SQLAlchemy database session
    @param vehicle: Vehicle to create
    @return: The created vehicle
    """
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def delete_vehicle(db: Session, vehicle_id: int) -> models.Vehicle:
    """
    Delete a vehicle by ID
    @param db: SQLAlchemy database session
    @param vehicle_id: ID of the vehicle to delete
    @return: The deleted vehicle
    """
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    db.delete(db_vehicle)
    db.commit()
    return db_vehicle


def update_vehicle(db: Session, vehicle: schemas.VehicleUpdate) -> models.Vehicle:
    """
    Update a vehicle by ID
    @param db: SQLAlchemy database session
    @param vehicle_id: ID of the vehicle to update
    @return: The updated vehicle
    """
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle.id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for var, value in vars(vehicle).items():
        setattr(db_vehicle, var, value) if value else None
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle
