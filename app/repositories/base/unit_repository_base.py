from abc import ABC, abstractmethod

from typing import Optional, List

from app.repositories.sql_repository import SqlRepository

from app.models.units import Unit


class UnitRepositoryBase(SqlRepository[Unit], ABC):

    @abstractmethod
    def add_unit(self, entity: Unit) -> Unit:
        raise NotImplementedError()
    
    