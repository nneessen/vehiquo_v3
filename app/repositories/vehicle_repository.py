from typing import Optional, List

from sqlalchemy.orm import Session

from app.repositories.sql_repository import SqlRepository

from app.models.vehicles import Vehicle

from app.repositories.base.vehicle_repository_base import VehicleRepositoryBase
    

class VehicleRepository(VehicleRepositoryBase, SqlRepository[Vehicle]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Vehicle)
        
    def add_vehicle(self, entity: Vehicle) -> Vehicle:
        return super()._add(entity)
    
    def delete_vehicle(self, vehicle_id: int) -> Vehicle:
        return super()._delete(vehicle_id)
    
    def get_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        return super()._get(vehicle_id)