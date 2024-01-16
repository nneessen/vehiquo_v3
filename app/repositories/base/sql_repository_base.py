from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional


T = TypeVar("T")

class SqlRepositoryBase(Generic[T], ABC):

    @abstractmethod
    def _add(self, entity: T) -> T:
        raise NotImplementedError()
    
    @abstractmethod
    def _delete(self, entity_id: int):
        raise NotImplementedError()
    
    @abstractmethod
    def _get(self, entity_id: int) -> Optional[T]:
        raise NotImplementedError()
    
    @abstractmethod
    def _get_all(self, 
        skip: int, 
        limit: int, 
        filter: Optional[dict] = None, 
        to_join: bool = False, 
        model_to_join: Optional[T] = None,
        joined_model_filters: Optional[dict] = None
        ) -> List[T]:
        """
        Get all entities
        @param skip: Number of entities to skip
        @param limit: Maximum number of entities to return
        @param filter: Filter to apply to query
        @param to_join: Whether to join tables or not
        @param model_to_join: Model to join with
        @param joined_model_filters: Filters to apply to joined model
        @return: A list of entities
        """
        raise NotImplementedError()
    
    @abstractmethod
    def _update(self, entity: T, entity_id: int) -> T:
        raise NotImplementedError()