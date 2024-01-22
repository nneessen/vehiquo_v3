from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import stores as store_model
from app.schemas import stores as store_schema
from app.unit_of_work.unit_of_work import UNIT_OF_WORK, UnitOfWork


def create_store(db: Session, store: store_schema.StoreAdd) -> store_model.Store:
    with UnitOfWork(db) as uow:
        store = uow.stores.add_store(store)
        uow.commit()
        uow.refresh(store)
        return store.serialize() if store else None


def delete_store(db: Session, store_id: int) -> None:
    with UnitOfWork(db) as uow:
        uow.stores.delete_store(store_id)
        uow.commit()
    return None


def get_store_by_id(db: Session, store_id: int) -> Optional[store_model.Store]:
    with UnitOfWork(db) as uow:
        store = uow.stores.get_store(store_id)
        return store.serialize() if store else None


def get_stores(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filter: Optional[dict] = None,
    to_join: bool = False,
    models_to_join: Optional[List[str]] = None,
    joined_model_filters: Optional[dict] = None,
) -> List[store_model.Store]:

    db_stores = UNIT_OF_WORK(db).stores.get_all_stores(
        skip, limit, filter, to_join, models_to_join, joined_model_filters
    )
    return [db_store.serialize() for db_store in db_stores]


def update_store(
    db: Session, store_id: int, store: store_schema.StoreUpdate
) -> store_model.Store:
    updated_store = UNIT_OF_WORK(db).stores.update_store(store_id, store)
    db.commit()
    db.refresh(updated_store)
    return updated_store.serialize() if updated_store else None
