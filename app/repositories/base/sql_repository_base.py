from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional


T = TypeVar("T")

class SqlRepositoryBase(Generic[T], ABC):

    @abstractmethod
    def _add(self, entity: T) -> T:
        raise NotImplementedError()