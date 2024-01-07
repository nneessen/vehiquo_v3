from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas import users as user_schema
from app.schemas import tokens as token_schema
from app.services import users as user_service
from app.services import tokens as token_service
from app.unit_of_work.unit_of_work import UnitOfWork

router = APIRouter(tags=["Login"])


@router.post("/token")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = token_service.create_access_token(
        subject={"sub": user.email}, expires_delta=access_token_expires
    )
    return token_schema.Token(access_token=access_token, token_type="bearer")