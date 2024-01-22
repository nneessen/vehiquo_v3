from typing import Annotated, Any, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.vehicles import Vehicle
from app.routers.security.dependencies import (CURRENT_USER, SESSION,
                                               get_current_active_user)
from app.schemas import vehicles as vehicle_schemas
from app.services import vehicles as vehicle_services
from app.utils.mapper import map_string_to_model

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


VEHICLE_RESPONSE_MODEL = Annotated[
    vehicle_schemas.VehicleOutput, Literal["Default Vehicle Response Model"]
]


@router.get(
    "/{vehicle_id}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[VEHICLE_RESPONSE_MODEL],
)
def get_vehicle(vehicle_id: int, db: SESSION) -> Optional[VEHICLE_RESPONSE_MODEL]:
    db_vehicle = vehicle_services.get_vehicle_by_id(db, vehicle_id=vehicle_id)
    if not db_vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with id {vehicle_id} not found",
        )
    return db_vehicle


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[VEHICLE_RESPONSE_MODEL]
)
def get_vehicles(
    db: SESSION,
    skip: int = 0,
    limit: int = 100,
    filter_key: Optional[str] = None,
    filter_value: Optional[str] = None,
    to_join: bool = False,
    models_to_join: Optional[Any] = None,
    joined_model_filter_key: Optional[str] = None,
    joined_model_filter_value: Optional[str] = None,
    include_unit_model: bool = False,
) -> List[VEHICLE_RESPONSE_MODEL]:
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

    vehicles = vehicle_services.get_vehicles(
        db,
        skip=skip,
        limit=limit,
        to_join=to_join,
        models_to_join=models_to_join_classes,
        joined_model_filters=joined_model_filters,
        include_unit_model=include_unit_model,
    )
    return vehicles
