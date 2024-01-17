from typing import Optional

from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import stores as store_model
from app.models import users as user_model
from app.models import units as unit_model

from app.schemas import stores as store_schema
from app.schemas import users as user_schema
from app.schemas import units as unit_schema

from app.unit_of_work.unit_of_work import UnitOfWork


def create_store(db: Session, store: store_schema.StoreCreate) -> store_model.Store:
    try:
        with UnitOfWork(db) as uow:
            store = uow.stores.add_store(store)
            uow.commit()
            uow.refresh(store)
            return store.as_dict() if store else None
    except Exception as e:
        return {"Status": "Error", "Message": f"Error creating store: {e}"}


def get_store_by_id(db: Session, store_id: int) -> Optional[store_model.Store]:
    return db.query(store_model.Store).filter(store_model.Store.id == store_id).first()


def get_stores(db: Session, skip: int = 0, limit: int = 100) -> list[store_model.Store]:
    return db.query(store_model.Store).offset(skip).limit(limit).all()





def update_store(db: Session, store_id: int, store: store_schema.StoreUpdate) -> store_model.Store:
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
    db_store = db.query(store_model.Store).filter(store_model.Store.id == store_id).first()

    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")

    db.delete(db_store)
    db.commit()
    return db_store


