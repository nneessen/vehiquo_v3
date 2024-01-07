from pydantic import BaseModel, Field, EmailStr
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
    pass

class UserDelete(UserBase):
    id: int 

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    
    __config__ = {
        "from_attributes": True,
        "allow_population_by_field_name": True,
        "arbitrary_types_allowed": True,
        }


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