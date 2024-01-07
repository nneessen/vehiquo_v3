from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from app.services import users as services
from app.schemas.users import UserInDB


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends(oauth2_scheme)]):
    user = await services.get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user)
    hashed_password = user.hashed_password
    if not services.verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return {
        "access_token": user.username,
        "token_type": "bearer",
    }