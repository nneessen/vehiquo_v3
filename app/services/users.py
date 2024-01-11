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
    
    
def hash_password(password: str) -> str:
    """
    Hash a password
    @param password: Password to hash
    @return: The hashed password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password
    @param password: Password to verify
    @param hashed_password: Hashed password to verify against
    @return: True if the password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))



def get_user(db, username: str):
    """
    Get a user by username
    @param db: SQLAlchemy database session
    @param username: Username of the user to get
    @return: The user with the given username
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """
    Get a user by ID
    @param db: SQLAlchemy database session
    @param user_id: ID of the user to get
    @return: The user with the given ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Get a user by email
    @param db: SQLAlchemy database session
    @param email: Email of the user to get
    @return: The user with the given email
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """
    Get a user by username
    @param db: SQLAlchemy database session
    @param username: Username of the user to get
    @return: The user with the given username
    """
    return db.query(models.User).filter(models.User.username == username).first()


def confirm(db: Session, user: models.User) -> models.User:
    """
    Confirm a user by setting confirmed to True
    @param db: SQLAlchemy database session
    @param user: User to confirm
    @return: The confirmed user
    """
    user.confirmed = True
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[Optional[models.User]]:
    """
    Get a list of users
    @param db: SQLAlchemy database session
    @param skip: Number of users to skip
    @param limit: Maximum number of users to return
    @return: List of users
    """
    return db.query(models.User).offset(skip).limit(limit).all()

@timeit
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Create a new user
    @param db: SQLAlchemy database session
    @param user: User to create
    @return: The created user
    """
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
    """
    Delete a user by ID
    @param db: SQLAlchemy database session
    @param user_id: ID of the user to delete
    @return: The deleted user
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def activate_user(db: Session, user_id: int) -> models.User:
    """
    Activate a user by setting is_active to True
    @param db: SQLAlchemy database session
    @param user_id: ID of the user to activate
    @return: The activated user
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)
    return db_user


def deactivate_user(db: Session, user_id: int) -> models.User:
    """
    Deactivate a user by setting is_active to False
    
    @param db: SQLAlchemy database session
    @param user_id: ID of the user to deactivate
    @return: The deactivated user
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    """
    Authenticate a user
    @param db: SQLAlchemy database session
    @param username: Username of the user to authenticate
    @param password: Password of the user to authenticate
    @return: The authenticated user
    """
    user = get_user(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def is_active(user: models.User) -> bool:
    """
    Check if a user is active
    @param user: User to check
    @return: True if the user is active, False otherwise
    """
    return user.is_active