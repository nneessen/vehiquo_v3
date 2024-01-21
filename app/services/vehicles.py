from typing import List, Optional

from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import vehicles as models

from app.schemas import vehicles as schemas

from app.unit_of_work.unit_of_work import UnitOfWork

def create_vehicle(db: Session, vehicle: schemas.VehicleAdd) -> models.Vehicle:
    with UnitOfWork(db) as uow:
        db_vehicle = uow.vehicles.add_vehicle(vehicle)
        uow.commit()
        uow.refresh(db_vehicle)
        return db_vehicle.serialize() if db_vehicle else None


def get_vehicle_by_id(db: Session, vehicle_id: int) -> Optional[models.Vehicle]:
    with UnitOfWork(db) as uow:
        db_vehicle = uow.vehicles.get_vehicle(vehicle_id)
        return db_vehicle.serialize() if db_vehicle else None


def get_vehicles(
    db: Session,
    skip: int = 0, 
    limit: int = 100,
    filter: Optional[dict] = None,
    to_join: bool = False,
    models_to_join: Optional[List[str]] = None,
    joined_model_filters: Optional[dict] = None,
    include_unit_model: bool = False,
    ) -> List[models.Vehicle]:
    db_vehicles = UnitOfWork(db).vehicles.get_all_vehicles(
        skip, limit, filter, to_join, models_to_join, joined_model_filters)
    return [db_vehicle.serialize(include_unit_model=include_unit_model) for db_vehicle in db_vehicles]

def delete_vehicle(db: Session, vehicle_id: int) -> models.Vehicle:

    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    db.delete(db_vehicle)
    db.commit()
    return db_vehicle


def update_vehicle(db: Session, vehicle: schemas.VehicleUpdate) -> models.Vehicle:
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle.id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    for var, value in vars(vehicle).items():
        setattr(db_vehicle, var, value) if value else None
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle
