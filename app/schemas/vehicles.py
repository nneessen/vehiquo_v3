from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class VehicleBase(BaseModel):
    year: int | None = Field(None, ge=2000, le=2024)
    make: str | None = Field(None, max_length=50)
    model: str | None = Field(None, max_length=50)
    trim: str | None = Field(None, max_length=50)
    vin: str | None = Field(None, max_length=17)
    mileage: int | None = Field(None, ge=0)
    color: str | None = Field(None, max_length=50)
    
    model_config: ConfigDict = ConfigDict(
        from_attributes=True, 
        populate_by_name=True,
        extra="ignore"
    )

    
class VehicleAdd(VehicleBase):
    drivetrain: str | None = Field(None, max_length=50)
    transmission: str | None = Field(None, max_length=50)
    transmission_type: str | None = Field(None, max_length=50)
    transmission_speeds: int | None = Field(None, ge=0)
    highway_mileage: int | None = Field(None, ge=0)
    city_mileage: int | None = Field(None, ge=0)
    engine_cylinders: int | None = Field(None, ge=0)
    category: str | None = Field(None, max_length=50)
    msrp: int | None = Field(None, ge=0)


class VehicleUpdate(VehicleBase, validate_assignment=True):
    pass


class VehicleDelete(VehicleBase):
    pass

class VehicleUnit(BaseModel):
    id: int | None = None
    list_date: datetime | None = None


class VehicleOutput(VehicleBase):
    id: int | None = None
    unit: VehicleUnit | None = None


class Vehicle(VehicleBase):
    pass