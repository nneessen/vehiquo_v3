from typing import Annotated, Any, List, Literal, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.stores import Store
from app.models.units import Unit
from app.models.vehicles import Vehicle
from app.routers.security.dependencies import (CURRENT_USER,
                                               get_current_active_user)
from app.schemas import units as units_schema
from app.schemas import users as user_schema
from app.schemas import vehicles as vehicles_schema
from app.services import units as unit_service
from app.utils.mapper import map_string_to_model

router = APIRouter(prefix="/units", tags=["Units"])

UnitResponseModel = Annotated[units_schema.UnitOutput, Literal["UnitResponse"]]
# ✅
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=units_schema.UnitCreateOutput,
)
def create_unit(
    current_user: CURRENT_USER,
    unit: units_schema.UnitAdd,
    vehicle: vehicles_schema.VehicleAdd,
    db: Session = Depends(get_db),
) -> units_schema.UnitCreateOutput:

    if current_user.is_admin:
        db_unit = unit_service.create_unit(db, unit=unit, vehicle=vehicle)
        if not db_unit:
            raise HTTPException(
                status_code=400, detail=f"Unit with name {unit.name} already exists"
            )
    return db_unit


# ✅
@router.get(
    "/{unit_id}", status_code=status.HTTP_200_OK, response_model=UnitResponseModel
)
def get_unit(
    # current_user: CURRENT_USER,
    unit_id: int,
    db: Session = Depends(get_db),
    include_vehicle: bool = False,
    include_store: bool = False,
) -> UnitResponseModel:

    # if not current_user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")

    unit = unit_service.get_unit_by_id(
        db,
        unit_id=unit_id,
        include_vehicle=include_vehicle,
        include_store=include_store,
    )

    if not unit:
        raise HTTPException(status_code=404, detail=f"Unit with id {unit_id} not found")
    return unit


# ✅
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UnitResponseModel])
def get_units(
    current_user: CURRENT_USER,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    filter_key: Optional[str] = None,
    filter_value: Optional[str] = None,
    to_join: bool = False,
    models_to_join: Optional[Any] = None,  # comma separated string of models to join
    joined_model_filter_key: Optional[str] = None,
    joined_model_filter_value: Optional[str] = None,
    include_vehicle: bool = False,
    include_store: bool = False,
) -> List[UnitResponseModel]:

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    filter = {filter_key: filter_value} if filter_key and filter_value else None
    joined_model_filters = (
        {joined_model_filter_key: joined_model_filter_value}
        if joined_model_filter_key and joined_model_filter_value
        else None
    )

    models_to_join_classes = []

    if to_join and models_to_join:
        models_to_join_classes = [
            map_string_to_model(model) for model in models_to_join.split(",")
        ]

    units = unit_service.get_units(
        db,
        skip=skip,
        limit=limit,
        filter=filter,
        to_join=to_join,
        models_to_join=models_to_join_classes,
        joined_model_filters=joined_model_filters,
        include_vehicle=include_vehicle,
        include_store=include_store,
    )

    if not units:
        raise HTTPException(status_code=404, detail=f"Units not found")
    return units


@router.delete("/{unit_id}", status_code=status.HTTP_200_OK, response_model=None)
def delete_unit(
    current_user: CURRENT_USER, unit_id: int, db: Session = Depends(get_db)
) -> None:
    if current_user.is_admin:
        unit_service.delete_unit(db, unit_id=unit_id)
        return {"Status": "Success", "Message": f"Unit with id {unit_id} deleted."}
    else:
        raise HTTPException(
            status_code=403, detail=f"User {current_user.email} is not an admin"
        )


@router.post("/expire_units", status_code=status.HTTP_200_OK)
async def expire_units(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
) -> Any:
    background_tasks.add_task(unit_service.check_and_expire_units, db)
    return {
        "Status": "Success",
        "Message": "Expire units task added to background tasks.",
    }


@router.put(
    "/{unit_id}", status_code=status.HTTP_200_OK, response_model=units_schema.UnitOutput
)
def update_unit(
    current_user: CURRENT_USER,
    unit_id: int,
    unit: units_schema.UnitAdd,
    db: Session = Depends(get_db),
) -> units_schema.UnitOutput:

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    db_unit = unit_service.update_unit(db, unit=unit, unit_id=unit_id)
    if db_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"Status": "Success", "Unit": db_unit}
