from pydantic import BaseModel, Field
from datetime import datetime, timedelta


class UnitBase(BaseModel):
    list_date: datetime | None = datetime.utcnow()
    expire_date: datetime | None = datetime.utcnow() + timedelta(hours=24)
    buy_now_price: int | None = Field(None, ge=0)
    added_by: int | None = 2
    zip_code_loc: int | None = 60610


class UnitAdd(UnitBase):
    pass

class UnitUpdate(UnitBase):
    pass

class UnitDelete(UnitBase):
    pass

class UnitExpire(UnitBase):
    pass
    
class UnitOutput(UnitBase):
    stock_number: str | None = None
    purchase_date: datetime | None = None
    sold_date: datetime | None = None
    purchase_price: int | None = None
    vehicle_age: int | None = None
    transportation_fee: int | None = None
    transportation_distance: int | None = None
    transport_company: str | None = None
    vehicle_cost: int | None = None
    maxoffer_value: int | None = None
    maxoffer_clock: int | None = None
    sold_status: bool | None = None
    purchased: bool | None = None
    is_expired: bool | None = None
    cdk_deal_number: int | None = None
    retailWholesale: str | None = None
    retail_front_gross: int | None = None
    retail_back_gross: int | None = None
    wholesale_gross: int | None = None
    total_retail_gross: int | None = None
    delivery_status: str | None = None
    buy_fee: int | None = None
    purchased_by: int | None = None
    added_by: int | None = None


class Unit(UnitBase):
    store_id: int
    vehicle_id: int
    
    __config__ = {
        "from_attributes": True,
        "allow_population_by_field_name": True,
        "arbitrary_types_allowed": True,
        "orm_mode": True,
        }
