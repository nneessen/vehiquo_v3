from typing import Optional, List

from sqlalchemy.orm import Session

from sqlalchemy import select, and_

from app.repositories.sql_repository import SqlRepository

from app.repositories.base.unit_repository_base import UnitRepositoryBase

from app.models.units import Unit

    
class UnitRepository(UnitRepositoryBase, SqlRepository[Unit]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Unit)
        
    def get(self, id: int) -> Optional[Unit]:
        return super().get(id)
    
    def get_all(self) -> List[Unit]:
        return super().get_all()
    
    def add_unit(self, unit: Unit) -> Unit:
        return super().add(unit)
    
    def update_unit(self, id: int, unit: Unit) -> Unit:
        return super().update(id, unit)
    
    def delete_unit(self, id: int) -> None:
        return super().delete(id)
        
    def list_units(self, skip: int, limit: int) -> List[Unit]:
        return self.db.query(Unit).offset(skip).limit(limit).all()