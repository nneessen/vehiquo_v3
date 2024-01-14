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




class Unit(Base):
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
    vehicle = relationship("Vehicle", back_populates="units")
    
    store_id = Column(Integer, ForeignKey("stores.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    purchased_by = Column(Integer, ForeignKey("users.id"))
    added_by = Column(Integer, ForeignKey("users.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "stock_number": self.stock_number,
            "purchase_date": self.purchase_date,
            "list_date": self.list_date,
            "sold_date": self.sold_date,
            "expire_date": self.expire_date,
            "purchase_price": self.purchase_price,
            "buy_now_price": self.buy_now_price,
            "vehicle_age": self.vehicle_age,
            "transportation_fee": self.transportation_fee,
            "transportation_distance": self.transportation_distance,
            "transport_company": self.transport_company,
            "vehicle_cost": self.vehicle_cost,
            "maxoffer_value": self.maxoffer_value,
            "maxoffer_clock": self.maxoffer_clock,
            "sold_status": self.sold_status,
            "purchased": self.purchased,
            "is_expired": self.is_expired,
            "cdk_deal_number": self.cdk_deal_number,
            "retailWholesale": self.retailWholesale,
            "retail_front_gross": self.retail_front_gross,
            "retail_back_gross": self.retail_back_gross,
            "wholesale_gross": self.wholesale_gross,
            "total_retail_gross": self.total_retail_gross,
            "zip_code_loc": self.zip_code_loc,
            "delivery_status": self.delivery_status,
            "buy_fee": self.buy_fee,
            "vehicle": self.vehicle.to_dict(),
            "store_id": self.store_id,
            "vehicle_id": self.vehicle_id,
            "purchased_by": self.purchased_by,
            "added_by": self.added_by,
            
        }