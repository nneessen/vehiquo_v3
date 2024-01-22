from typing import Any, Optional

from fastapi import HTTPException

from app.models.stores import Store
from app.models.units import Unit
from app.models.users import User
from app.models.vehicles import Vehicle


def map_string_to_model(model_name: str) -> Any:
    model_mapping = {"vehicle": Vehicle, "unit": Unit, "user": User, "store": Store}

    model_class = model_mapping.get(model_name.lower())
    if not model_class:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")

    return model_class
