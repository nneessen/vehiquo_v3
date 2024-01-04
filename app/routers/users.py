from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas import users as schemas
from app.services import users as services

router = APIRouter(tags=["Users"])


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.UserOutput:
    db_user = services.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.create_user(db=db, user=user)


@router.get("/users/", status_code=status.HTTP_200_OK)
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip=skip, limit=limit)
    return {"Status": "Success", "Users": users}


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = services.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with id {user_id} not found"
            )
    return {"Status": "Success", "User": user}


@router.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user