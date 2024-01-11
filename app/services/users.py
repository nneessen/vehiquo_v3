import bcrypt

from fastapi import HTTPException

from typing import List, Optional

from sqlalchemy.orm import Session

from sqlalchemy.orm.exc import FlushError

from sqlalchemy.exc import IntegrityError, InvalidRequestError

from sqlalchemy import func, and_, not_, inspect, update, delete, insert

from app.models import users as models

from app.schemas import users as schemas

from app.utils.decorators import timeit


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

def get_user(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[Optional[models.User]]:
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def confirm(db: Session, user: models.User) -> models.User:
    user.confirmed = True
    db.commit()
    db.refresh(user)
    return user

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = hash_password(user.password)
    user_data = user.model_dump(exclude={"password"})
    user_data["hashed_password"] = hashed_password
    stmt = insert(models.User).values(**user_data)
    try:
        db.execute(stmt)
        db.commit()
    except (IntegrityError, InvalidRequestError, FlushError) as e:
        error_details = {
            IntegrityError: "Email or username already registered",
            InvalidRequestError: "Invalid request",
            FlushError: "Flush error"
        }
        detail = error_details.get(type(e), "Unknown error")
        raise HTTPException(status_code=400, detail=detail)
    return get_user_by_email(db, email=user.email)

def delete_user(db: Session, user_id: int) -> models.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

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