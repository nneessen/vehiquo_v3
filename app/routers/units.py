from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas import units as schemas
from app.schemas.users import User
from app.services import units as services
from app.routers.users import get_current_user
from app.unit_of_work.unit_of_work import UnitOfWork



router = APIRouter(prefix="/units", tags=["Units"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UnitOutput)
def create_unit(unit: schemas.UnitAdd, db: Session = Depends(get_db)) -> schemas.UnitOutput:
    with UnitOfWork(db) as uow:
        db_unit = services.create_unit(db, unit=unit)
        uow.commit()
        return {"Status": "Success", "Unit": db_unit}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UnitOutput])
def get_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[schemas.UnitOutput]:
    units = services.get_units(db, skip=skip, limit=limit)
    return {"Status": "Success", "Units": units}


@router.get("/{unit_id}", status_code=status.HTTP_200_OK, response_model=schemas.UnitOutput)
def get_unit(unit_id: int, db: Session = Depends(get_db)) -> schemas.UnitOutput:
    unit = services.get_unit_by_id(db, unit_id=unit_id)
    if not unit:
        raise HTTPException(
            status_code=404, 
            detail=f"Unit with id {unit_id} not found"
            )
    return {"Status": "Success", "Unit": unit}


@router.delete("/{unit_id}", response_model=schemas.UnitOutput)
def delete_unit(unit_id: int, db: Session = Depends(get_db)) -> schemas.UnitOutput:
    with UnitOfWork(db) as uow:
        try:
            db_unit = services.delete_unit(db, unit_id=unit_id)
            if db_unit is None:
                raise HTTPException(status_code=404, detail="Unit not found")
            uow.commit()
            return {"Status": "Success", "Unit": db_unit}
        except Exception as e:
            uow.rollback()
            raise e