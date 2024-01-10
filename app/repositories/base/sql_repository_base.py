from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional


T = TypeVar("T")

class SqlRepositoryBase(Generic[T], ABC):

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError()

    @abstractmethod
    def add(self, entity: T) -> T:
        raise NotImplementedError()
    
    @abstractmethod
    def add_all(self, entities: List[T]) -> List[T]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError()