from typing import Any, Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.unit_of_work.unit_of_work import UnitOfWork

from app.schemas import units as units_schema
from app.schemas import users as users_schema
from app.schemas import vehicles as vehicles_schema

from app.services import units as unit_service
from app.services import users as user_service
from app.services import vehicles as vehicle_service

from app.routers.users import get_current_user



router = APIRouter(prefix="/units", tags=["Units"])

#✅
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=units_schema.UnitOutput)
def create_unit(unit: units_schema.UnitAdd, vehicle: vehicles_schema.VehicleAdd, db: Session = Depends(get_db)) -> units_schema.UnitOutput:
    db_unit = unit_service.create_unit(db, unit=unit, vehicle=vehicle)
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"Status": "Success", "Unit": db_unit}



#⚠️ need to work on this function
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[units_schema.UnitOutput])
def get_units(db: Session = Depends(get_db)) -> units_schema.UnitOutput:
    units = unit_service.get_units(db)
    if not units:
        raise HTTPException(
            status_code=404, 
            detail=f"Units not found"
            )
    return units


@router.get("/{unit_id}", status_code=status.HTTP_200_OK, response_model=units_schema.UnitOutput)
def get_unit(unit_id: int, db: Session = Depends(get_db)) -> units_schema.UnitOutput:
    unit = unit_service.get_unit_by_id(db, unit_id=unit_id)
    if not unit:
        raise HTTPException(
            status_code=404, 
            detail=f"Unit with id {unit_id} not found"
            )
    return {"Status": "Success", "Unit": unit}


@router.delete("/{unit_id}", response_model=units_schema.UnitOutput)
def delete_unit(unit_id: int, db: Session = Depends(get_db)) -> units_schema.UnitOutput:
    with UnitOfWork(db) as uow:
        try:
            db_unit = unit_service.delete_unit(db, unit_id=unit_id)
            if db_unit is None:
                raise HTTPException(status_code=404, detail="Unit not found")
            uow.commit()
            return {"Status": "Success", "Unit": db_unit}
        except Exception as e:
            uow.rollback()
            raise e
        
@router.post("/expire_units", status_code=status.HTTP_200_OK)
async def expire_units(background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Any:
    background_tasks.add_task(unit_service.check_and_expire_units, db)
    return {"Status": "Success", "Message": "Expire units task added to background tasks."}