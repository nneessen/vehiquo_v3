from abc import ABC, abstractmethod

from typing import Optional, List

from app.repositories.sql_repository import SqlRepository

from app.models.units import Unit


class UnitRepositoryBase(SqlRepository[Unit], ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[Unit]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all(self) -> List[Unit]:
        raise NotImplementedError()
    
    @abstractmethod
    def add_unit(self, unit: Unit) -> Unit:
        raise NotImplementedError()
    
    @abstractmethod
    def update_unit(self, id: int, unit: Unit) -> Unit:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_unit(self, id: int) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def list_units(self, skip: int, limit: int) -> List[Unit]:
        raise NotImplementedError()