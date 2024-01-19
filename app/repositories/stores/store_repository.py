from typing import Optional, List, Any

from sqlalchemy.orm import Session

from app.repositories.base.sql_repository import SqlRepository

from app.repositories.stores.store_repository_base import StoreRepositoryBase

from app.models.stores import Store
from app.models.units import Unit
from app.models.vehicles import Vehicle
from app.models.users import User

from app.exceptions.custom_exceptions import (
    DeleteStoreException,
    AddStoreException,
    UpdateStoreException, 
    GetStoreException
)


class StoreRepository(StoreRepositoryBase, SqlRepository[Store]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Store)


    def add_store(self, store: Store) -> Store:
        return super()._add(store)


    def delete_store(self, store_id: int) -> Optional[Store]:
            return super()._delete(store_id)


    def get_store(self, store_id: int) -> Optional[Store]:
        return super()._get(store_id)

    def get_all_stores(self, 
        skip: int = 0, 
        limit: int = 100, 
        filter: Optional[dict] = None,
        to_join: bool = False,
        models_to_join: Optional[List[str]] = None,
        joined_model_filters: Optional[dict] = None
        ) -> List[Store]:
        return super()._get_all(
            skip, limit, filter, to_join, models_to_join, joined_model_filters)


    def update_store(self, store: Store, store_id: int) -> Store:
        return super()._update(store, store_id)
