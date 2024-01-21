import time

from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime


from app.models import units as unit_model
from app.models import vehicles as vehicle_model

from app.schemas import units as unit_schema
from app.schemas import vehicles as vehicle_schema
from app.schemas import users as user_schema

from app.unit_of_work.unit_of_work import UNIT_OF_WORK, UnitOfWork


def create_unit(db: Session, unit: unit_schema.UnitAdd, vehicle: vehicle_schema.VehicleAdd) -> unit_model.Unit:
        with UnitOfWork(db) as uow:
            db_unit = uow.units.add_unit(unit)
            db_vehicle = uow.vehicles.add_vehicle(vehicle)
            db_unit.vehicle_id = db_vehicle.id
            uow.commit()
            uow.refresh(db_unit), uow.refresh(db_vehicle)
            return db_unit.serialize() if db_unit else None


#✅
def get_unit_by_id(
    db: Session, 
    unit_id: int,
    include_vehicle: bool = False,
    include_store: bool = False,
) -> Optional[unit_model.Unit]:
        with UnitOfWork(db) as uow:
            db_unit = uow.units.get_unit(unit_id)
            return db_unit.serialize(
                include_vehicle=include_vehicle, include_store=include_store) if db_unit else None


#✅
def get_units(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    filter: Optional[dict] = None,
    to_join: bool = False,
    models_to_join: Optional[List[str]] = None,
    joined_model_filters: Optional[dict] = None,
    include_vehicle: bool = False,
    include_store: bool = False,
    ) -> List[unit_model.Unit]:

    db_units = UNIT_OF_WORK(db).units.get_all_units(
        skip, limit, filter, to_join, models_to_join, joined_model_filters)
    return [db_unit.serialize(
        include_vehicle=include_vehicle, include_store=include_store) for db_unit in db_units]


def delete_unit(db: Session, unit_id: int) -> unit_model.Unit:
    vehicle_id = db.query(unit_model.Unit).filter(unit_model.Unit.id == unit_id).first().vehicle_id
    if not vehicle_id:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db_unit = UNIT_OF_WORK(db).units.delete_unit(unit_id)
    UNIT_OF_WORK(db).vehicles.delete_vehicle(vehicle_id)
    db.commit()
    return db_unit


def expire_units(db: Session) -> bool:
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
    db_unit = UNIT_OF_WORK(db).units.update_unit(unit, unit_id)
    db.commit()
    db.refresh(db_unit)
    return db_unit