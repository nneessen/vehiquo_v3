from typing import Any, List, Optional

import bcrypt
from fastapi import HTTPException
from sqlalchemy import or_, and_, func, desc, asc, text, select, update
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import FlushError

from app.models import users as models
from app.models.stores import Store
from app.schemas import users as schemas
from app.unit_of_work.unit_of_work import UnitOfWork



# ✅ Takes 0.1808s to create user
def create_user(db: Session, user: schemas.UserCreate, include_store: bool = False) -> models.User:
        with UnitOfWork(db) as uow:
            db_user = uow.users.add_user(user)
            db_user.hashed_password = hash_password(user.password)
            db_user.password = None
            uow.commit()
            return db_user.serialize(include_store=include_store)


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    with UnitOfWork(db) as uow:
        user = uow.users.get_user(user_id)
        return user.serialize()


def get_user_by_email_or_username(db: Session, email: str, username: str) -> Optional[models.User]:
    stmt = select(models.User).where(or_(models.User.email == email, models.User.username == username))
    result = db.execute(stmt).first()
    return result[0] if result else None


# ✅
def authenticate_user(
    db: Session, username: str, password: str
) -> Optional[models.User]:
    user = get_user(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ✅
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# ✅
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# ✅
def get_user(db, username: str):
    stmt = select(models.User).where(models.User.username == username)
    result = db.execute(stmt).first()
    return result[0] if result else None


# ✅
def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filter: Optional[dict] = None,
    to_join: bool = False,
    models_to_join: Optional[List[str]] = None,
    joined_model_filters: Optional[dict] = None,
    include_store: bool = False,
) -> List[Optional[models.User]]:

    with UnitOfWork(db) as uow:
        users = uow.users.get_users(
            skip, limit, filter, to_join, models_to_join, joined_model_filters
        )
        return [user.serialize(include_store=include_store) for user in users]


# ✅ Takes 0.0093s to delete user
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


def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> models.User:
    with UnitOfWork(db) as uow:
        db_user = uow.users.update_user(user_id, user)
        uow.commit()
        return db_user.serialize()

# ✅
def confirm(db: Session, user: models.User) -> models.User:
    user.confirmed = True
    db.commit()
    db.refresh(user)
    return user


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
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")