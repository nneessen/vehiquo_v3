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