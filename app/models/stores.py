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


class Store(SerializerMixin, Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    street_address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(Integer, nullable=True)
    phone = Column(String, nullable=True)
    admin_clerk_1 = Column(String, nullable=True)
    is_primary_hub = Column(Boolean, nullable=True, default=False)
    qb_customer_id = Column(Integer, nullable=True)
    
    # autogroup_id = Column(Integer, ForeignKey("autogroups.id"))
    # cluster_id = Column(Integer, ForeignKey("clusters.id"))
    
    users = relationship("User", backref="store", lazy="joined")
    units = relationship("Unit", backref="store", cascade='all, delete-orphan',lazy="joined")
    
    def as_dict(self):
        return self.serialize(exclude=["users", "units"])