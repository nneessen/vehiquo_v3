from typing import Optional, List

from sqlalchemy.orm import Session

from sqlalchemy import select, and_

from app.repositories.sql_repository import SqlRepository

from app.repositories.base.unit_repository_base import UnitRepositoryBase

from app.models.units import Unit

from app.exceptions.custom_exceptions import (
    DeleteUnitException,
    AddUnitException
)
    
class UnitRepository(UnitRepositoryBase, SqlRepository[Unit]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Unit)
        
    def add_unit(self, unit: Unit) -> Unit:
        try:
            return super()._add(unit)
        except Exception as e:
            message = f"Error adding unit with id {unit.id}"
            error_code = "unit_add_error"
            raise AddUnitException(message, error_code)
    
    def delete_unit(self, unit_id: int) -> Unit:
        try:
            return super()._delete(unit_id)
        except Exception as e:
            message = f"Error deleting unit with id {unit_id}"
            error_code = "unit_delete_error"
            raise DeleteUnitException(message, error_code)

    def get_unit(self, unit_id: int) -> Optional[Unit]:
        try:
            return super()._get(unit_id)
        except Exception as e:
            message = f"Error getting unit with id {unit_id}"
            error_code = "unit_get_error"
            raise DeleteUnitException(message, error_code)