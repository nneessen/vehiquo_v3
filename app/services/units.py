import time

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime

from app.models import units as unit_model
from app.models import vehicles as vehicle_model

from app.schemas import units as unit_schema
from app.schemas import vehicles as vehicle_schema

from app.unit_of_work.unit_of_work import UnitOfWork

def get_unit_by_id(db: Session, unit_id: int) -> Optional[unit_model.Unit]:
    """
    Get a unit by ID
    @param db: SQLAlchemy database session
    @param unit_id: ID of the unit to get
    @return: The unit with the given ID
    """
    return db.query(unit_model.Unit).filter(unit_model.Unit.id == unit_id).first()


def get_units(db: Session, skip: int = 0, limit: int = 100) -> List[unit_model.Unit]:
    """
    Get all units
    @param db: SQLAlchemy database session
    @param skip: Number of units to skip
    @param limit: Maximum number of units to return
    @return: A list of units
    """
    return db.query(unit_model.Unit).offset(skip).limit(limit).all()


def create_unit(db: Session, unit: unit_schema.UnitAdd, vehicle: vehicle_schema.VehicleAdd) -> unit_model.Unit:
    """✅
    Create a new unit
    @param db: SQLAlchemy database session
    @param unit: Unit to create
    @return: The created unit
    """
    try:
        db_unit = unit_model.Unit(**unit.model_dump())
        db_vehicle = vehicle_model.Vehicle(**vehicle.model_dump())
        db_unit.vehicle = db_vehicle
        db.add_all([db_unit, db_vehicle])
        db.commit()
        db.refresh(db_unit)
        db.refresh(db_vehicle)
        return db_unit
    except Exception as e:
        db.rollback()
        raise e

def delete_unit(db: Session, unit_id: int) -> unit_model.Unit:
    """✅
    Delete a unit by ID
    @param db: SQLAlchemy database session
    @param unit_id: ID of the unit to delete
    @return: The deleted unit
    """
    db_unit = db.query(unit_model.Unit).filter(unit_model.Unit.id == unit_id).first()
    vehicle = db.query(vehicle_model.Vehicle).filter(vehicle_model.Vehicle.id == db_unit.vehicle_id).first()

    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")

    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    db.delete(vehicle)
    db.delete(db_unit)
    db.commit()
    return db_unit


def expire_units(db: Session) -> bool:
    """
    Expire units that have passed their expiration date.
    @param db: SQLAlchemy database session
    @return: True if any units were expired, False otherwise
    """
    db_units = db.query(unit_model.Unit).filter(unit_model.Unit.expire_date <= datetime.utcnow()).all()
    if not db_units:
        return False

    for db_unit in db_units:
        db_unit.is_expired = True

    db.commit()
    return True



def check_and_expire_units(db: Session) -> None:
    while True:
        expire_units(db)
        time.sleep(60*15)




def update_unit(db: Session, unit: unit_schema.UnitUpdate) -> unit_model.Unit:
    """
    Update a unit
    @param db: SQLAlchemy database session
    @param unit: Unit to update
    @return: The updated unit
    """
    db_unit = db.query(unit_model.Unit).filter(unit_model.Unit.id == unit.id).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    for var, value in vars(unit).items():
        setattr(db_unit, var, value) if value else None
    db.commit()
    db.refresh(db_unit)
    return db_unit


def add_vehicle_to_unit(db: Session, vehicle_id: int, unit_id: int) -> unit_model.Unit:
    """
    Add a vehicle to a unit
    @param db: SQLAlchemy database session
    @param vehicle_id: ID of the vehicle to add
    @param unit_id: ID of the unit to add the vehicle to
    @return: The updated unit
    """
    db_unit = db.query(unit_model.Unit).filter(unit_model.Unit.id == unit_id).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    db_unit.vehicle_id = vehicle_id
    db.commit()
    db.refresh(db_unit)
    return db_unit