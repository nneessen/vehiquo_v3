from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime

from typing import Optional, List


class StoreBase(BaseModel):
    name: str | None = Field(None, max_length=50)
    street_address: str | None = Field(None, max_length=50)
    city: str | None = Field(None, max_length=50)
    state: str | None = Field(None, max_length=50)
    zip_code: int | None = Field(None)
    phone: str | None = Field(None, max_length=50)
    admin_clerk_1: str | None = Field(None, max_length=50, description="Admin Clerk 1")
    is_primary_hub: bool | None = Field(None)
    qb_customer_id: int | None = Field(None)

    model_config: ConfigDict = ConfigDict(
        from_attributes=True, 
        populate_by_name=True,
        extra="ignore"
    )

class StoreCreate(StoreBase):
    pass


class StoreUpdate(StoreBase):
    pass


class StoreDelete(StoreBase):
    pass


class StoreUserOutput(BaseModel):
    id: int | None = Field(None)
    store_id: int | None = Field(None)



class StoreUnitOutput(BaseModel):
    id: int | None = Field(None)
    vehicle_id: int | None = None
    store_id: int | None = None
    

class StoreOutput(BaseModel):
    id: int | None = None
    name: str | None = Field(..., max_length=50)
    street_address: str | None = Field(None, max_length=50)
    city: str | None = Field(None, max_length=50)
    state: str | None = Field(None, max_length=50)
    zip_code: int | None = Field(None)
    phone: str | None = Field(None, max_length=50)
    admin_clerk_1: str | None = Field(None, max_length=50, description="Admin Clerk 1")
    is_primary_hub: bool | None = Field(None)
    qb_customer_id: int | None = Field(None)
    
    users: List[StoreUserOutput] | None = Field(None, description="Users associated with this store")
    units: List[StoreUnitOutput] | None = Field(None, description="Units associated with this store")
    
    