from abc import ABC, abstractmethod

from typing import Optional, List

from app.repositories.sql_repository import SqlRepository

from app.models.vehicles import Vehicle


class VehicleRepositoryBase(SqlRepository[Vehicle], ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[Vehicle]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all(self) -> List[Vehicle]:
        raise NotImplementedError()
    
    @abstractmethod
    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        raise NotImplementedError()
    
    # @abstractmethod
    # def update_vehicle(self, id: int, vehicle: Vehicle) -> Vehicle:
    #     raise NotImplementedError()
    
    # @abstractmethod
    # def delete_vehicle(self, id: int) -> None:
    #     raise NotImplementedError()
    
    # @abstractmethod
    # def list_vehicles(self, skip: int, limit: int) -> List[Vehicle]:
    #     raise NotImplementedError()
    
    # @abstractmethod
    # def get_last_added_vehicle(self) -> None:
    #     raise NotImplementedError()