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
    def __init__(self, db: Callable[[], Session]) -> None:
        self.db = db
    
    def __enter__(self):
        self.db = Session()
        self.users = UserRepository(self.db)
        self.units = UnitRepository(self.db)
        self.vehicles = VehicleRepository(self.db)
        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.db.close()
    
    def commit(self):
        self.db.commit()
        
    def rollback(self):
        self.db.rollback()