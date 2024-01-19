from abc import ABC, abstractmethod

from typing import Optional, List, Any

from app.repositories.base.sql_repository import SqlRepository

from app.models.stores import Store


class StoreRepositoryBase(SqlRepository[Store], ABC):
    
    @abstractmethod
    def add_store(self, entity: Store) -> Optional[Store]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_store(self, entity_id: int) -> Optional[Store]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_store(self, entity_id: int) -> Optional[Store]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_stores(self,
              skip: int = 0, 
              limit: int = 100, 
              filter: Optional[dict] = None,
              to_join: bool = False,
              models_to_join: Optional[List[str]] = None,
              joined_model_filters: Optional[dict] = None
        ) -> List[Store]:
        raise NotImplementedError()