from pydantic import BaseModel, Field, ConfigDict


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


class StoreOutput(StoreBase):
    pass

class Store(StoreBase):
    unit_id: int
    user_id: int
    # autogroup_id: int
    # cluster_id: int
