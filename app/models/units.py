from datetime import datetime, timedelta
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
)
from sqlalchemy.orm import relationship

from app.database import Base

from app.models.mixins.core import SerializerMixin

class Unit(SerializerMixin, Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stock_number = Column(String, nullable=True)
    purchase_date = Column(DateTime, nullable=True)
    list_date = Column(DateTime, nullable=True)
    sold_date = Column(DateTime, nullable=True)
    expire_date = Column(DateTime, nullable=True, default=datetime.utcnow() + timedelta(minutes=1))
    purchase_price = Column(Integer, nullable=True, default=0)
    buy_now_price = Column(Integer, nullable=True, default=0)
    vehicle_age = Column(Integer, nullable=True, default=0)
    transportation_fee = Column(Integer, nullable=True, default=0)
    transportation_distance = Column(Integer, nullable=True, default=0)
    transport_company = Column(String, nullable=True, default="N/A")
    vehicle_cost = Column(Integer, nullable=True, default=0)
    maxoffer_value = Column(Integer, nullable=True, default=0)
    maxoffer_clock = Column(Integer, nullable=True, default=0)
    sold_status = Column(Boolean, nullable=True, default=False)
    purchased = Column(Boolean, nullable=True, default=False)
    is_expired = Column(Boolean, nullable=True, default=False)
    cdk_deal_number = Column(Integer, nullable=True, default=0)
    retailWholesale = Column(String, nullable=True, default="Retail")
    retail_front_gross = Column(Integer, nullable=True, default=0)
    retail_back_gross = Column(Integer, nullable=True, default=0)
    wholesale_gross = Column(Integer, nullable=True, default=0)
    total_retail_gross = Column(Integer, nullable=True, default=0)
    zip_code_loc = Column(Integer, nullable=True, default=60610)
    delivery_status = Column(String, nullable=True, default="N/A")
    buy_fee = Column(Integer, nullable=True, default=250)
    
    # store = relationship("Store", back_populates="units")
    store_id = Column(Integer, ForeignKey("stores.id"))

    vehicle = relationship("Vehicle", back_populates="units")
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    purchased_by = Column(Integer, ForeignKey("users.id"))
    added_by = Column(Integer, ForeignKey("users.id"))

    
