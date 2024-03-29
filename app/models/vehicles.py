from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.mixins.core import SerializerMixin


class Vehicle(SerializerMixin, Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    year = Column(Integer, nullable=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    trim = Column(String, nullable=True)
    vin = Column(String, nullable=True)
    mileage = Column(Integer, nullable=True)
    color = Column(String, nullable=True)
    drivetrain = Column(String, nullable=True)
    transmission = Column(String, nullable=True)
    transmission_type = Column(String, nullable=True)
    transmission_speeds = Column(Integer, nullable=True)
    highway_mileage = Column(Integer, nullable=True)
    city_mileage = Column(Integer, nullable=True)
    engine_cylinders = Column(Integer, nullable=True)
    category = Column(String, nullable=True)
    msrp = Column(Integer, nullable=True)

    # Relationships
    units = relationship("Unit", back_populates="vehicle", lazy="select")
