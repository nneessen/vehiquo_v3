import time

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
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


def get_units(db: Session, skip: int = 0, limit: int = 100) -> List[unit_schema.UnitOutput]:
    """
    Get all units
    @param db: SQLAlchemy database session
    @param skip: Number of units to skip
    @param limit: Maximum number of units to return
    @return: A list of units
    """
    units = db.query(unit_model.Unit).offset(skip).limit(limit).all()
    unit_outputs = []
    for unit in units:
        vehicle_data = vehicle_schema.VehicleOutput.model_validate(unit.vehicle) if unit.vehicle else None
        unit_data = unit_schema.UnitOutput.model_validate(unit)
        unit_data.vehicle = vehicle_data
        unit_outputs.append(unit_data)
    return unit_outputs


def get_store_units(db: Session, store_id: int, skip: int = 0, limit: int = 100) -> List[unit_model.Unit]:
    """
    Get all units for a store
    @param db: SQLAlchemy database session
    @param store_id: ID of the store to get units for
    @param skip: Number of units to skip
    @param limit: Maximum number of units to return
    @return: A list of units
    """
    return db.query(unit_model.Unit).filter(unit_model.Unit.store_id == store_id).offset(skip).limit(limit).all()

def create_unit(db: Session, unit: unit_schema.UnitAdd, vehicle: vehicle_schema.VehicleAdd) -> unit_model.Unit:
    """✅
    Create a new unit
    @param db: SQLAlchemy database session
    @param unit: Unit to create
    @return: The created unit
    """
    try:
        with UnitOfWork(db) as uow:
            db_unit = uow.units.add_unit(unit)
            db_vehicle = uow.vehicles.add_vehicle(vehicle)
            db_unit.vehicle_id = db_vehicle.id
            db.commit()
            db.refresh(db_unit)
            return db_unit
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def delete_unit(db: Session, unit_id: int) -> unit_model.Unit:
    """✅
    Delete a unit by ID
    @param db: SQLAlchemy database session
    @param unit_id: ID of the unit to delete
    @return: The deleted unit
    """
    vehicle_id = db.query(unit_model.Unit).filter(unit_model.Unit.id == unit_id).first().vehicle_id
    if not vehicle_id:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    try:
        with UnitOfWork(db) as uow:
            db_unit = uow.units.delete_unit(unit_id)
            uow.vehicles.delete_vehicle(vehicle_id)
            uow.commit()
            return db_unit
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


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




def update_unit(db: Session, unit:unit_schema.UnitUpdate, unit_id: int) -> unit_model.Unit:
    """
    Update a unit
    @param db: SQLAlchemy database session
    @param unit: Unit to update
    @return: The updated unit
    """
    try:
        with UnitOfWork(db) as uow:
            db_unit = uow.units.update_unit(unit, unit_id)
            uow.commit()
            return db_unit
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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