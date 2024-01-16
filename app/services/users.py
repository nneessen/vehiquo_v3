import bcrypt

from typing import List, Optional, Any

from fastapi import HTTPException

from sqlalchemy.orm import Session

from sqlalchemy.orm.exc import FlushError

from sqlalchemy.exc import IntegrityError, InvalidRequestError

from sqlalchemy import func, and_, not_, inspect, update, delete, insert

from app.models import users as models
from app.models.stores import Store

from app.schemas import users as schemas

from app.utils.decorators import timeit

from app.unit_of_work.unit_of_work import UnitOfWork

#✅
def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

#✅
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

#✅
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

#✅
def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

#✅
def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    filter: Optional[dict] = None,
    to_join: bool = False,
    model_to_join: Optional[str] = None,
    joined_model_filters: Optional[dict] = None
    ) -> List[Optional[models.User]]:
    try:
        with UnitOfWork(db) as uow:
            users = uow.users.get_users(skip, limit, filter, to_join, model_to_join, joined_model_filters)
            return [user.as_dict() for user in users]
    except Exception as e:
        return {"Status": "Failed", "Detail": "Error getting users"}

#✅
def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    try:
        with UnitOfWork(db) as uow:
            user = uow.users.get_user(user_id)
            return user.as_dict()
    except Exception as e:
        return {"Status": "Failed", "Detail": f"Error getting user with id {user_id}"}


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def confirm(db: Session, user: models.User) -> models.User:
    user.confirmed = True
    db.commit()
    db.refresh(user)
    return user


#✅ Takes 0.1808s to create user
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    try:
        with UnitOfWork(db) as uow:
            db_user = uow.users.add_user(user)
            db_user.hashed_password = hash_password(user.password)
            db_user.password = None
            uow.commit()
    except (IntegrityError, InvalidRequestError, FlushError) as e:
        error_details = {
            IntegrityError: "Email or username already registered",
            InvalidRequestError: "Invalid request",
            FlushError: "Flush error"
        }
        detail = error_details.get(type(e), "Unknown error")
        return {"Status": "Failed", "Detail": detail}
    return get_user_by_email(db, email=user.email)

#✅ Takes 0.0093s to delete user
def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        return {"Status": "Failed", "Detail": f"User with id {user_id} not found"}
    try:
        with UnitOfWork(db) as uow:
            uow.users.delete_user(user_id)
            uow.commit()
            return {"Status": "Success", "Detail": "User deleted successfully"}
    except Exception as e:
        return {"Status": "Failed", "Detail": f"Error deleting user with id {user_id}"}
            
    
def activate_user(db: Session, user_id: int) -> models.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return db_user

def deactivate_user(db: Session, user_id: int) -> models.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user

def is_active(user: models.User) -> bool:
    return user.is_active


def map_string_to_model(model_name: str) -> Any:
    if model_name.lower() == "vehicle":
        return Store
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Model {model_name} not found"
            )