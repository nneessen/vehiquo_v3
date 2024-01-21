from typing import Any, Annotated, List, Optional, Literal

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas import users as schemas
from app.schemas import tokens as token_schema

from app.services import users as user_service

from app.routers.security.dependencies import get_current_active_user, create_access_token

from app.utils.mapper import map_string_to_model

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

from app.routers.security.dependencies import CURRENT_USER, SESSION

UserResponseModel = Annotated[schemas.UserOutput, Literal["UserResponseModel"]]

router = APIRouter(tags=["Users"])


@router.post("/token", response_model=token_schema.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SESSION) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

#✅
@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponseModel)
def create_user(user: schemas.UserCreate, db: SESSION) -> schemas.UserOutput:
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
            )
    db_user = user_service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Username already registered"
            )
    db_user = user_service.create_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"Status": "Success", "User": db_user}


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel)
def get_user(user_id: int, db: SESSION) -> schemas.UserOutput:
    user = user_service.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with id {user_id} not found"
            )
    return user


@router.get("/users/", status_code=status.HTTP_200_OK, response_model=List[UserResponseModel])
def get_users(db: SESSION, 
              skip: int = 0,
              limit: int = 100,
              filter_key: Optional[str] = None,
              filter_value: Optional[str] = None,
              to_join: bool = False,
              models_to_join: Optional[str] = None, # comma separated string of models to join
              joined_model_filter_key: Optional[str] = None,
              joined_model_filter_value: Optional[str] = None,
              include_store: bool = False,
    ) -> List[UserResponseModel]:
    
    filter = {filter_key: filter_value} if filter_key and filter_value else None
    joined_model_filters = {joined_model_filter_key: joined_model_filter_value} if joined_model_filter_key and joined_model_filter_value else None


    models_to_join_classes = []
    if models_to_join:
        models_to_join_classes = [map_string_to_model(model) for model in models_to_join.split(",")]
    
    users = user_service.get_users(
        db, 
        skip=skip, 
        limit=limit,
        filter=filter,
        to_join=to_join, 
        models_to_join=models_to_join_classes,
        joined_model_filters=joined_model_filters,
        include_store=include_store
    )

    if not users:
        raise HTTPException(
            status_code=404, 
            detail="No users found"
            )
    return users


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: SESSION):
    delete_result = user_service.delete_user(db, user_id=user_id)
    if delete_result["Status"] == "Failed":
        return delete_result
    return delete_result


@router.get("/users/me/", response_model=UserResponseModel)
def read_users_me(current_user: CURRENT_USER):
    return current_user
