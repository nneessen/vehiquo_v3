from typing import Optional, List

from sqlalchemy.orm import Session

from app.repositories.sql_repository import SqlRepository

from app.models.vehicles import Vehicle

from app.repositories.base.vehicle_repository_base import VehicleRepositoryBase
    

class VehicleRepository(VehicleRepositoryBase, SqlRepository[Vehicle]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Vehicle)
        
    def get(self, id: int) -> Optional[Vehicle]:
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self) -> List[Vehicle]:
        return super().get_all()
    
    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle