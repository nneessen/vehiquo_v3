from abc import ABC, abstractmethod
from typing import Any, List, Optional

from app.models.units import Unit
from app.repositories.base.sql_repository import SqlRepository


class UnitRepositoryBase(SqlRepository[Unit], ABC):
    @abstractmethod
    def add_unit(self, entity: Unit) -> Unit:
        raise NotImplementedError()

    @abstractmethod
    def delete_unit(self, entity_id: int):
        raise NotImplementedError()

    @abstractmethod
    def get_unit(self, entity_id: int) -> Optional[Unit]:
        raise NotImplementedError()

    @abstractmethod
    def get_all_units(
        self,
        skip: int,
        limit: int,
        filter: Optional[dict] = None,
        to_join: bool = False,
        models_to_join: Optional[List[str]] = None,
        joined_model_filters: Optional[dict] = None,
    ) -> List[Unit]:
        raise NotImplementedError()

    @abstractmethod
    def update_unit(self, entity: Unit, entity_id: int) -> Unit:
        raise NotImplementedError()
