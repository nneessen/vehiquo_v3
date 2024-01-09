from pydantic import BaseModel, Field, EmailStr, ConfigDict
from collections.abc import Iterable, Sequence
from typing import List

class UserBase(BaseModel):
    first_name : str | None = Field(None, min_length=2, max_length=50)
    last_name : str | None = Field(None, min_length=2, max_length=50)
    email : EmailStr | None = Field(
        None, 
        min_length=2, 
        max_length=100, 
        description="Email must be a valid email address."
    )
    username : str | None = Field(
        None, 
        min_length=5, 
        max_length=25, 
        description="Username must be between 5 and 25 characters and can only contain letters, numbers, underscores, and dashes."
    )
    password: str | None = Field(
        None, 
        min_length=8, 
        max_length=50, 
        description="Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, and one number."
    )
    model_config: ConfigDict = {
        "from_attributes": True,
        "populate_by_name": True,
    }

class UserOutput(BaseModel):
    first_name : str | None = Field(None, min_length=2, max_length=50)
    last_name : str | None = Field(None, min_length=2, max_length=50)
    email : EmailStr | None = Field(
        None, 
        min_length=2, 
        max_length=100, 
        description="Email must be a valid email address."
    )
    username : str | None = Field(
        None, 
        min_length=5, 
        max_length=25, 
        description="Username must be between 5 and 25 characters and can only contain letters, numbers, underscores, and dashes."
    )
    phone_number : str | None = None

class UserCreate(UserBase):
    is_active: bool = True
    is_buyer: bool = False
    is_admin: bool = False
    is_superuser: bool = False
    is_blocked: bool = False
    store_id: int | None = Field(None, description="The ID of the store the user belongs to.")

class UserDelete(UserBase):
    id: int 

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    store_id: int


class UserInDB(UserBase):
    hashed_password: str


class UserLogin(UserBase):
    username : str | None = Field(
        None, 
        min_length=5, 
        max_length=25, 
        description="Username must be between 5 and 25 characters and can only contain letters, numbers, underscores, and dashes."
    )
    password: str | None = Field(
        None, 
        min_length=8, 
        max_length=50, 
        description="Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, and one number."
    )


class ListUserResponse(BaseModel):
    users: List[User]