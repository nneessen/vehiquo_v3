from typing import Any, List, Annotated, Optional, Literal

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.models.vehicles import Vehicle

from app.schemas import units as units_schema
from app.schemas import vehicles as vehicles_schema

from app.services import units as unit_service

from app.routers.security.dependencies import oauth2_scheme

from app.utils.mapper import map_string_to_model


router = APIRouter(prefix="/units", tags=["Units"])

UnitResponse = Annotated[units_schema.UnitOutput, Literal["UnitResponse"]]
#✅
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=units_schema.UnitCreateOutput)
def create_unit(
    unit: units_schema.UnitAdd, 
    vehicle: vehicles_schema.VehicleAdd, 
    db: Session = Depends(get_db)) -> units_schema.UnitCreateOutput:

    db_unit = unit_service.create_unit(db, unit=unit, vehicle=vehicle)

    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return db_unit



#✅
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UnitResponse])
def get_units(db: Session = Depends(get_db), 
              skip: int = 0,
              limit: int = 100,
              filter_key: Optional[str] = None,
              filter_value: Optional[str] = None,
              to_join: bool = False,
              model_to_join: Optional[str] = None,
              joined_model_filter_key: Optional[str] = None,
              joined_model_filter_value: Optional[str] = None
    ) -> UnitResponse:

    filter = {filter_key: filter_value} if filter_key and filter_value else None
    joined_model_filters = {joined_model_filter_key: joined_model_filter_value} if joined_model_filter_key and joined_model_filter_value else None

    if model_to_join:
        model_to_join = map_string_to_model(model_to_join)
    
    units = unit_service.get_units(
        db, 
        skip=skip, 
        limit=limit, 
        filter=filter, 
        to_join=to_join, 
        model_to_join=model_to_join, 
        joined_model_filters=joined_model_filters
    )
    
    if not units:
        raise HTTPException(
            status_code=404, 
            detail=f"Units not found"
            )
    return units



#✅
@router.get("/{unit_id}", status_code=status.HTTP_200_OK, response_model=units_schema.UnitOutput)
def get_unit(unit_id: int, db: Session = Depends(get_db)) -> units_schema.UnitOutput:
    unit = unit_service.get_unit_by_id(db, unit_id=unit_id)
    if not unit:
        raise HTTPException(
            status_code=404, 
            detail=f"Unit with id {unit_id} not found"
            )
    return unit


@router.delete("/{unit_id}", status_code=status.HTTP_200_OK, response_model=None)
def delete_unit(unit_id: int, db: Session = Depends(get_db)) -> None:
    unit_service.delete_unit(db, unit_id=unit_id)
    return {
        "Status": "Success", 
        "Message": f"Unit with id {unit_id} deleted."
    }
        
@router.post("/expire_units", status_code=status.HTTP_200_OK)
async def expire_units(background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Any:
    background_tasks.add_task(unit_service.check_and_expire_units, db)
    return {"Status": "Success", "Message": "Expire units task added to background tasks."}

@router.put("/{unit_id}", status_code=status.HTTP_200_OK, response_model=units_schema.UnitOutput)
def update_unit(unit_id: int, unit: units_schema.UnitAdd, db: Session = Depends(get_db)) -> units_schema.UnitOutput:
    db_unit = unit_service.update_unit(db, unit=unit, unit_id=unit_id)
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"Status": "Success", "Unit": db_unit}