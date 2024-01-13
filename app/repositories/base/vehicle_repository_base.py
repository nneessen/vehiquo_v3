from abc import ABC, abstractmethod

from typing import Optional, List

from app.repositories.sql_repository import SqlRepository

from app.models.vehicles import Vehicle


class VehicleRepositoryBase(SqlRepository[Vehicle], ABC):
    
    @abstractmethod
    def add_vehicle(self, entity: Vehicle) -> Vehicle:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_vehicle(self, vehicle_id: int) -> Vehicle:
        raise NotImplementedError()