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
        try:
            return super()._add(store)
        except Exception as e:
            message = f"Error adding store with id {store.id}"
            error_code = "store_add_error"
            raise AddStoreException(message, error_code)
        
    def delete_store(self, store_id: int) -> Optional[Store]:
        try:
            return super()._delete(store_id)
        except Exception as e:
            message = f"Error deleting store with id {store_id}"
            error_code = "store_delete_error"
            raise DeleteStoreException(message, error_code)
    
    def get_store(self, store_id: int) -> Optional[Store]:
        try:
            return super()._get(store_id)
        except Exception as e:
            message = f"Error getting store with id {store_id}"
            error_code = "store_get_error"
            raise GetStoreException(message, error_code)
    
    def get_all_stores(self, 
                      skip: int, 
                      limit: int, 
                      filter: Optional[dict] = None, 
                      to_join: bool = False, 
                      model_to_join: Optional[Any] = None,
                      joined_model_filters: Optional[dict] = None
        ) -> List[Store]:
        try:
            return super()._get_all(
                skip, limit, filter, to_join, model_to_join, joined_model_filters)
        except Exception as e:
            message = f"Error getting all stores"
            error_code = "stores_get_all_error"
            raise GetStoreException(message, error_code)