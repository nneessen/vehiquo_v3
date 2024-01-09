from typing import Optional

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import stores as store_model
from app.models import users as user_model
from app.models import units as unit_model

from app.schemas import stores as store_schema
from app.schemas import users as user_schema
from app.schemas import units as unit_schema


def get_store_by_id(db: Session, store_id: int) -> Optional[store_model.Store]:
    """
    Get a store by ID
    @param db: SQLAlchemy database session
    @param store_id: ID of the store to get
    @return: The store with the given ID
    """
    return db.query(store_model.Store).filter(store_model.Store.id == store_id).first()


def get_stores(db: Session, skip: int = 0, limit: int = 100) -> list[store_model.Store]:
    """
    Get all stores
    @param db: SQLAlchemy database session
    @param skip: Number of stores to skip
    @param limit: Maximum number of stores to return
    @return: A list of stores
    """
    return db.query(store_model.Store).offset(skip).limit(limit).all()


def create_store(db: Session, store: store_schema.StoreAdd) -> store_model.Store:
    """✅
    Create a new store
    @param db: SQLAlchemy database session
    @param store: Store to create
    @return: The created store
    """
    try:
        db_store = store_model.Store(**store.model_dump())
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return db_store
    except Exception as e:
        db.rollback()
        raise e


def update_store(db: Session, store_id: int, store: store_schema.StoreUpdate) -> store_model.Store:
    """✅
    Update a store by ID
    @param db: SQLAlchemy database session
    @param store_id: ID of the store to update
    @param store: Store data to update
    @return: The updated store
    """
    try:
        db_store = db.query(store_model.Store).filter(store_model.Store.id == store_id).first()
        for var, value in vars(store).items():
            setattr(db_store, var, value) if value else None
        db.commit()
        db.refresh(db_store)
        return db_store
    except Exception as e:
        db.rollback()
        raise e


def delete_store(db: Session, store_id: int) -> store_model.Store:
    """
    Delete a store by ID
    @param db: SQLAlchemy database session
    @param store_id: ID of the store to delete
    @return: The deleted store
    """
    db_store = db.query(store_model.Store).filter(store_model.Store.id == store_id).first()

    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")

    db.delete(db_store)
    db.commit()
    return db_store


