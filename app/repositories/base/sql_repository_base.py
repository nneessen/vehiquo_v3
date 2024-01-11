from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional


T = TypeVar("T")

class SqlRepositoryBase(Generic[T], ABC):

    @abstractmethod
    def begin_transaction(self):
        raise NotImplementedError()

    @abstractmethod
    def commit_transaction(self):
        raise NotImplementedError()
    
    @abstractmethod
    def rollback_transaction(self):
        raise NotImplementedError()
    
    @abstractmethod
    def end_transaction(self):
        raise NotImplementedError()
    
    @abstractmethod
    def construct_get_stmt(self, id: int):
        raise NotImplementedError()
    
    @abstractmethod
    def construct_update_stmt(self, id: int, entity: T):
        raise NotImplementedError()
    
    @abstractmethod
    def construct_delete_stmt(self, id: int):
        raise NotImplementedError()
    
    @abstractmethod
    def construct_add_stmt(self, entity: T):
        raise NotImplementedError()
    
    @abstractmethod
    def construct_list_stmt(self, **filters):
        raise NotImplementedError()
    
    @abstractmethod
    def construct_count_stmt(self, **filters):
        raise NotImplementedError()
    
    @abstractmethod
    def construct_exists_stmt(self, **filters):
        raise NotImplementedError()

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
    
    @abstractmethod
    def list(self, **filters) -> List[T]:
        raise NotImplementedError()
    
    @abstractmethod
    def count(self, **filters) -> int:
        raise NotImplementedError()
    
    @abstractmethod
    def exists(self, **filters) -> bool:
        raise NotImplementedError()