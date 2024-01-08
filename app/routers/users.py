from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas import users as schemas
from app.services import users as services
from app.unit_of_work.unit_of_work import UnitOfWork


router = APIRouter(tags=["Users"])


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserOutput:
    with UnitOfWork(db) as uow:
        db_user = services.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(
                status_code=400, 
                detail="Email already registered"
                )
        db_user = services.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(
                status_code=400, 
                detail="Username already registered"
                )
        db_user = services.create_user(db, user=user)
        uow.commit()
        return db_user


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = services.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with id {user_id} not found"
            )
    return {"Status": "Success", "User": user}


@router.get("/users/", status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip=skip, limit=limit)
    return {"Status": "Success", "Users": users}


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/current_user/", response_model=schemas.User)
def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))
    ):
    user = services.get_current_user(db, token=token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user