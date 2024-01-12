from typing import Optional, List

from sqlalchemy.orm import Session

from sqlalchemy import select, and_

from app.repositories.sql_repository import SqlRepository

from app.repositories.base.unit_repository_base import UnitRepositoryBase

from app.models.units import Unit

    
class UnitRepository(UnitRepositoryBase, SqlRepository[Unit]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Unit)
        
    def add_unit(self, unit: Unit) -> Unit:
        return super()._add(unit)