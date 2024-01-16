from abc import ABC, abstractmethod

from typing import Optional, List

from app.repositories.base.sql_repository import SqlRepository

from app.models.vehicles import Vehicle


class VehicleRepositoryBase(SqlRepository[Vehicle], ABC):
    
    @abstractmethod
    def add_vehicle(self, entity: Vehicle) -> Vehicle:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_vehicle(self, vehicle_id: int) -> Vehicle:
        raise NotImplementedError()
    
    @abstractmethod
    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        raise NotImplementedError()