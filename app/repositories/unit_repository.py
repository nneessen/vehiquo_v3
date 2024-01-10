from typing import Optional, List

from sqlalchemy.orm import Session

from app.repositories.sql_repository import SqlRepository

from app.repositories.base.unit_repository_base import UnitRepositoryBase

from app.models.units import Unit

    
class UnitRepository(UnitRepositoryBase, SqlRepository[Unit]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Unit)
        
    def get(self, id: int) -> Optional[Unit]:
        return self.db.query(Unit).filter(Unit.id == id).first()
    
    def get_all(self) -> List[Unit]:
        return super().get_all()
    
    def add_unit(self, unit: Unit) -> Unit:
        self.db.add(unit)
        self.db.commit()
        self.db.refresh(unit)
        return unit
    
    def update_unit(self, id: int, unit: Unit) -> Unit:
        self.db.query(Unit).filter(Unit.id == id).update(unit)
        return unit
    
    def delete_unit(self, id: int) -> None:
        self.db.query(Unit).filter(Unit.id == id).delete()
        
    def list_units(self, skip: int, limit: int) -> List[Unit]:
        return self.db.query(Unit).offset(skip).limit(limit).all()