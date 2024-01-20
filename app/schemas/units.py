from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timedelta


from app.schemas import vehicles as vehicles_schema
from app.schemas import stores as stores_schema
from app.schemas import users as users_schema

class UnitBase(BaseModel):
    list_date: datetime | None = datetime.utcnow()
    expire_date: datetime | None = datetime.utcnow() + timedelta(minutes=5)
    buy_now_price: int | None = Field(None, ge=0)
    added_by: int | None = 2
    zip_code_loc: int | None = 60610
    
    model_config: ConfigDict = ConfigDict(
        from_attributes=True, 
        populate_by_name=True,
        extra="ignore",
    )
    
    

class UnitAdd(UnitBase):
    store_id: int | None = Field(1, description="Default store ID is 1.")


class UnitUpdate(UnitBase):
    pass

class UnitDelete(UnitBase):
    pass

class UnitExpire(UnitBase):
    pass
    
class UnitOutput(BaseModel):
    id: int | None = Field(None, serialization_alias="unit_id")
    list_date: datetime | None = None
    purchase_date: datetime | None = None
    sold_date: datetime | None = None
    purchase_price: int | None = None
    transportation_fee: int | None = None
    transport_company: str | None = None
    delivery_status: str | None = None
    vehicle_cost: int | None = None
    sold_status: bool | None = None
    purchased: bool | None = None
    is_expired: bool | None = None
    cdk_deal_number: int | None = None
    retailWholesale: str | None = None
    retail_front_gross: int | None = None
    retail_back_gross: int | None = None
    wholesale_gross: int | None = None
    total_retail_gross: int | None = None
    buy_fee: int | None = None
    purchased_by: int | None = None

    vehicle: vehicles_schema.VehicleOutput | None =  Field(None, description="Vehicle object")
    store: stores_schema.StoreOutput | None = None
    


class UnitCreateOutput(BaseModel):
    id: int | None = None
    purchase_price: int | None = None
    transportation_fee: int | None = None
    purchased: bool | None = None
    retailWholesale: str | None = None
    buy_now_price: int | None = None
    buy_fee: int | None = None
    purchased_by: int | None = None
    added_by: int | None = None

    vehicle: vehicles_schema.VehicleOutput | None = None
    store: stores_schema.StoreOutput | None = None
    user: users_schema.UserOutput | None = None


class Unit(UnitBase):
    store_id: int
    vehicle_id: int