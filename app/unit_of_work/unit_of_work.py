import logging

from abc import ABC, abstractmethod
from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.logging_config import setup_logging


from app.repositories.user_repository import UserRepositoryBase, UserRepository
from app.repositories.vehicle_repository import VehicleRepositoryBase, VehicleRepository
from app.repositories.unit_repository import UnitRepositoryBase, UnitRepository



setup_logging()
logger = logging.getLogger(__name__)


class UnitOfWorkBase(ABC):
    users: UserRepositoryBase
    units: UnitRepositoryBase
    vehicles: VehicleRepositoryBase
    
    def __enter__(self):
        return self
    
    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()
        else:
            self.rollback()
        
    @abstractmethod
    def commit(self):
        raise NotImplementedError()
    
    @abstractmethod
    def rollback(self):
        raise NotImplementedError()
    

class UnitOfWork(UnitOfWorkBase):
    def __init__(self, db: Callable[[], Session]):
        self.db = db
        self._users = None
        self._units = None
        self._vehicles = None
    
    def __enter__(self):
        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.db.close()
    
    @property
    def users(self) -> UserRepositoryBase:
        if self._users is None:
            self._users = UserRepository(self.db)
        return self._users
    
    @property
    def units(self) -> UnitRepositoryBase:
        if self._units is None:
            self._units = UnitRepository(self.db)
        return self._units
    
    @property
    def vehicles(self) -> VehicleRepositoryBase:
        if self._vehicles is None:
            self._vehicles = VehicleRepository(self.db)
        return self._vehicles
    
    def commit(self):
        self.db.commit()
        print("UnitOfWork.commit() called")
        
    def rollback(self):
        self.db.rollback()