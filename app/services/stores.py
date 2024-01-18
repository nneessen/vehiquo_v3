from typing import Optional, List

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
            return store.serialize() if store else None
    except Exception as e:
        return {"Status": "Error", "Message": f"Error creating store: {e}"}


def delete_store(db: Session, store_id: int) -> store_model.Store:
    try:
        with UnitOfWork(db) as uow:
            store = uow.stores.delete_store(store_id)
            uow.commit()
            return store
    except Exception as e:
        return {"Status": "Error", "Message": f"Error deleting store: {e}"}


def get_store_by_id(db: Session, store_id: int) -> Optional[store_model.Store]:
    try:
        with UnitOfWork(db) as uow:
            store = uow.stores.get_store(store_id)
            return store.serialize() if store else None
    except Exception as e:
        return {"Status": "Error", "Message": f"Error finding store with id of {store_id}"}
        
def get_stores(db: Session, 
               skip: int = 0, 
               limit: int = 100,
               filter: Optional[dict] = None,
               to_join: bool = False,
               model_to_join: Optional[str] = None,
               joined_model_filters: Optional[dict] = None
    ) -> List[store_model.Store]:
    
    with UnitOfWork(db) as uow:
        db_stores = uow.stores.get_all_stores(
            skip, limit, filter, to_join, model_to_join, joined_model_filters)
        return [db_store.serialize() for db_store in db_stores]
   
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




