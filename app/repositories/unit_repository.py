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


class UnitRepositoryBase(SqlRepository[Unit], ABC):
    @abstractmethod
    def get_unit_by_id(self, id: int) -> Optional[Unit]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_units(self) -> List[Unit]:
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

    @abstractmethod
    def auto_expire_units(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_units_listed_by_month(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_unsold_units_count(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_last_added_unit(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_active_units_for_current_user(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_active_units_for_admin(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_sold_units_for_current_user(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_sold_units_for_admin(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_purchased_units_for_current_user(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_purchased_units_for_admin(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def assign_unit_to_store(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def relist_unit(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def unwind_unit(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def mark_unit_as_sold_retail(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def mark_unit_as_sold_wholesale(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def check_cdk_number(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def to_dict(self) -> None:
        raise NotImplementedError()
    
    
class UnitRepository(UnitRepositoryBase, SqlRepository[Unit]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Unit)
        
    def get_unit_by_id(self, id: int) -> Optional[Unit]:
        return self.db.query(Unit).filter(Unit.id == id).first()
    
    def get_all_units(self) -> List[Unit]:
        return self.db.query(Unit).all()
    
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
    
    def auto_expire_units(self) -> None:
        units = self.db.query(Unit).filter(Unit.purchased == False).all()
        updated_units = []
        for unit in units:
            if datetime.utcnow() > unit.expire_date:
                unit.is_expired = True
                updated_units.append(unit)
    #TODO - create ExpiredUnit Schema