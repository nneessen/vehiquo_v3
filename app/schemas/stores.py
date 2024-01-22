from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


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
        from_attributes=True, populate_by_name=True, extra="ignore"
    )


class StoreAdd(StoreBase):
    pass


class StoreUpdate(StoreBase):
    pass


class StoreDelete(StoreBase):
    pass


# for user in StoreOutput.users:
class StoreUserOutput(BaseModel):
    id: int | None = Field(None)
    first_name: str | None = Field(None, max_length=50)
    last_name: str | None = Field(None, max_length=50)


# for unit in StoreOutput.units:
class StoreUnitOutput(BaseModel):
    id: int | None = Field(None)


class SingleStoreOutput(BaseModel):
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

    users: List[StoreUserOutput] | None = Field(
        None, description="Users associated with this store"
    )
    # units: List[StoreUnitOutput] | None = Field(None, description="Units associated with this store")
