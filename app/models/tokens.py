from sqlalchemy import Column, Integer, String

from app.database import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    access_token = Column(String, index=True)
    token_type = Column(String)
