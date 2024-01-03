from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    first_name : str
    last_name : str
    email : str
    username : str
    hashed_password: str
    is_active : bool
    is_admin : bool
    is_superuser : bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    __config__ = {"from_attributes": True}