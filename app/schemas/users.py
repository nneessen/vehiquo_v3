from pydantic import BaseModel


class UserBase(BaseModel):
    first_name : str | None = None
    last_name : str | None = None
    email : str | None = None
    username : str | None = None
    password: str | None = None
    hashed_password: str | None = None
    confirmed : bool | None = False
    phone_number : str | None = None
    twilio_opt_in : bool | None = False
    is_blocked : bool | None = False
    is_active : bool | None = False
    is_buyer: bool | None = False
    is_admin : bool | None = False
    is_superuser : bool | None = False


class UserCreate(UserBase):
    password: str


class UserDelete(UserBase):
    id: int

    __config__ = {"from_attributes": True}


class User(UserBase):
    id: int

    __config__ = {"from_attributes": True}
    
