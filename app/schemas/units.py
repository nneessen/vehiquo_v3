from pydantic import BaseModel, Field
from collections.abc import Iterable, Sequence
from typing import List
from datetime import datetime, timedelta


class UnitBase(BaseModel):
    list_date: datetime | None = datetime.utcnow()
    expire_date: datetime | None = datetime.utcnow() + timedelta(hours=24)
    buy_now_price: int | None = Field(None, ge=0)
    added_by: int | None = 1
    zip_code_loc: int | None = 60610


class UnitAdd(UnitBase):
    pass

class UnitUpdate(UnitBase):
    id: int

class UnitDelete(UnitBase):
    id: int

class UnitExpire(UnitBase):
    id: int

class Unit(UnitBase):
    __config__ = {
        "from_attributes": True,
        "allow_population_by_field_name": True,
        "arbitrary_types_allowed": True,
        }
