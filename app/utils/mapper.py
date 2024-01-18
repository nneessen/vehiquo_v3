from typing import Any, Optional

from fastapi import HTTPException

from app.models.vehicles import Vehicle
from app.models.units import Unit
from app.models.users import User
from app.models.stores import Store


def map_string_to_model(model_name: str) -> Any:
    if model_name.lower() == "vehicle":
        return Vehicle
    elif model_name.lower() == "unit":
        return Unit
    elif model_name.lower() == "user":
        return User
    elif model_name.lower() == "store":
        return Store
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Model {model_name} not found"
            )