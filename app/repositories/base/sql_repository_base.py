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
    def _update(self, entity: T, entity_id: int) -> T:
        raise NotImplementedError()