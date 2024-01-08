from abc import ABC, abstractmethod
from typing import Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import (
    select,
    and_,
    func
    )
from app.sql_repository import SqlRepository
from app.models.vehicles import Vehicle
from app.schemas import vehicles as schemas


class VehicleRepositoryBase(SqlRepository[Vehicle], ABC):
    @abstractmethod
    def get_vehicle_by_id(self, id: int) -> Optional[Vehicle]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_vehicles(self) -> List[Vehicle]:
        raise NotImplementedError()
    
    @abstractmethod
    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        raise NotImplementedError()
    
    @abstractmethod
    def update_vehicle(self, id: int, vehicle: Vehicle) -> Vehicle:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_vehicle(self, id: int) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def list_vehicles(self, skip: int, limit: int) -> List[Vehicle]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_last_added_vehicle(self) -> None:
        raise NotImplementedError()
    

class VehicleRepository(VehicleRepositoryBase, SqlRepository[Vehicle]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Vehicle)
        
    def get_vehicle_by_id(self, id: int) -> Optional[Vehicle]:
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all_vehicles(self) -> List[Vehicle]:
        return self.db.query(self.model).all()