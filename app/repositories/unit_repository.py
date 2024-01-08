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
from app.models.units import Unit
from app.schemas import units as schemas


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