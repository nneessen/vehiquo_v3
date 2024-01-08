from pydantic import BaseModel, Field
from collections.abc import Iterable, Sequence
from typing import List, Optional, Annotated
from datetime import datetime, timedelta


class VehicleBase(BaseModel):
    year: int | None = Field(None, ge=2000, le=2024)
    make: str | None = Field(None, max_length=50)
    model: str | None = Field(None, max_length=50)
    trim: str | None = Field(None, max_length=50)
    vin: str | None = Field(None, max_length=17)
    mileage: int | None = Field(None, ge=0)
    color: str | None = Field(None, max_length=50)
    drivetrain: str | None = Field(None, max_length=50)
    transmission: str | None = Field(None, max_length=50)
    transmission_type: str | None = Field(None, max_length=50)
    transmission_speeds: int | None = Field(None, ge=0)
    highway_mileage: int | None = Field(None, ge=0)
    city_mileage: int | None = Field(None, ge=0)
    engine_cylinders: int | None = Field(None, ge=0)
    category: str | None = Field(None, max_length=50)
    msrp: int | None = Field(None, ge=0)
    
class VehicleAdd(VehicleBase):
    pass

class VehicleUpdate(VehicleBase):
    pass

class VehicleDelete(VehicleBase):
    pass

class VehicleOutput(VehicleBase):
    units: List[Optional[int]] = []

class Vehicle(VehicleBase):
    __config__ = {
        "from_attributes": True,
        "allow_population_by_field_name": True,
        "arbitrary_types_allowed": True,
    }