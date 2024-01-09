from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_buyer = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)
    phone_number = Column(String, unique=True, index=True)
    twilio_opt_in = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    store_id = Column(Integer, ForeignKey("stores.id"))