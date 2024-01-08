from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.models import units as models
from app.schemas import units as schemas


def get_unit_by_id(db: Session, unit_id: int) -> Optional[models.Unit]:
    """
    Get a unit by ID
    @param db: SQLAlchemy database session
    @param unit_id: ID of the unit to get
    @return: The unit with the given ID
    """
    return db.query(models.Unit).filter(models.Unit.id == unit_id).first()


def get_units(db: Session, skip: int = 0, limit: int = 100) -> List[models.Unit]:
    """
    Get all units
    @param db: SQLAlchemy database session
    @param skip: Number of units to skip
    @param limit: Maximum number of units to return
    @return: A list of units
    """
    return db.query(models.Unit).offset(skip).limit(limit).all()


def create_unit(db: Session, unit: schemas.UnitAdd) -> models.Unit:
    """
    Create a new unit
    @param db: SQLAlchemy database session
    @param unit: Unit to create
    @return: The created unit
    """
    db_unit = models.Unit(**unit.model_dump())
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit


def delete_unit(db: Session, unit_id: int) -> models.Unit:
    """
    Delete a unit by ID
    @param db: SQLAlchemy database session
    @param unit_id: ID of the unit to delete
    @return: The deleted unit
    """
    db_unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    db.delete(db_unit)
    db.commit()
    return db_unit


def expire_unit(db: Session, unit_id: int) -> models.Unit:
    """
    Expire a unit by ID
    @param db: SQLAlchemy database session
    @param unit_id: ID of the unit to expire
    @return: The expired unit
    """
    db_unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    db_unit.expire_date = datetime.utcnow()
    db.commit()
    return db_unit


def update_unit(db: Session, unit: schemas.UnitUpdate) -> models.Unit:
    """
    Update a unit
    @param db: SQLAlchemy database session
    @param unit: Unit to update
    @return: The updated unit
    """
    db_unit = db.query(models.Unit).filter(models.Unit.id == unit.id).first()
    if not db_unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    for var, value in vars(unit).items():
        setattr(db_unit, var, value) if value else None
    db.commit()
    db.refresh(db_unit)
    return db_unit