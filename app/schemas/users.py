from pydantic import BaseModel, Field, EmailStr, ConfigDict

from typing import List

from app.schemas import stores as store_schema


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
    phone_number: str | None = Field(None, min_length=10, max_length=10)
    model_config: ConfigDict = ConfigDict(
        from_attributes=True, 
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class UserOutput(BaseModel):
    id: int | None = None
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
    
    store_id: int | None = None
    store: store_schema.StoreOutput | None = None


class UserCreate(UserBase):
    store_id: int | None = Field(None, description="The ID of the store the user belongs to.")


class UserUpdate(UserBase):
    id: int


class UserDelete(UserBase):
    id: int 


class UserInDB(UserBase):
    hashed_password: str


class User(UserBase):
    store_id: int


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