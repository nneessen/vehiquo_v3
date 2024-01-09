from pydantic import BaseModel, Field


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


class StoreAdd(StoreBase):
    pass


class StoreUpdate(StoreBase):
    pass


class StoreDelete(StoreBase):
    pass


class StoreOutput(StoreBase):
    pass


class Store(StoreBase):
    unit_id: int
    user_id: int
    # autogroup_id: int
    # cluster_id: int

    __config__ = {
        "from_attributes": True,
        "allow_population_by_field_name": True,
        "arbitrary_types_allowed": True,
        "orm_mode": True,
    }