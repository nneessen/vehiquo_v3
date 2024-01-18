from typing import Optional, List, Any

from sqlalchemy.orm import Session

from sqlalchemy import select, and_

from app.repositories.base.sql_repository import SqlRepository

from app.repositories.units.unit_repository_base import UnitRepositoryBase

from app.models.units import Unit
from app.models.vehicles import Vehicle

from app.exceptions.custom_exceptions import (
    DeleteUnitException,
    AddUnitException,
    UpdateUnitException
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


    def get_all_units(self, 
                      skip: int, 
                      limit: int, 
                      filter: Optional[dict] = None, 
                      to_join: bool = False, 
                      models_to_join: Optional[List[str]] = None,
                      joined_model_filters: Optional[dict] = None
        ) -> List[Unit]:
        return super()._get_all(
            skip, limit, filter, to_join, models_to_join, joined_model_filters)



    def update_unit(self, unit: Unit, unit_id: int) -> Unit:
        try:
            return super()._update(unit, unit_id)
        except Exception as e:
            message = f"Error updating unit with id {unit.id}"
            error_code = "unit_update_error"
            raise DeleteUnitException(message, error_code)