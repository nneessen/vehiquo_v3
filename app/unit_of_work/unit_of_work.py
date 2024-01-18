from abc import ABC, abstractmethod

from typing import Callable

from sqlalchemy.orm import Session

from app.repositories.units import unit_repository_base, unit_repository
from app.repositories.users import user_repository_base, user_repository
from app.repositories.vehicles import vehicle_repository_base, vehicle_repository
from app.repositories.stores import store_repository_base, store_repository


class UnitOfWorkBase(ABC):
    users: user_repository_base.UserRepositoryBase
    units: unit_repository_base.UnitRepositoryBase
    vehicles: vehicle_repository_base.VehicleRepositoryBase
    stores: store_repository_base.StoreRepositoryBase
    
    def __enter__(self):
        return self
    
    def __exit__(self, exn_type, exn_value, traceback):
        if exn_type is None:
            self.commit()
        else:
            self.rollback()
        
    @abstractmethod
    def refresh(self, entity):
        raise NotImplementedError()
    
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
        self._stores = None
        
    def __enter__(self):
        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.db.close()
    
    @property
    def users(self) -> user_repository_base.UserRepositoryBase:
        if self._users is None:
            self._users = user_repository.UserRepository(self.db)
        return self._users
    
    @property
    def units(self) -> unit_repository_base.UnitRepositoryBase:
        if self._units is None:
            self._units = unit_repository.UnitRepository(self.db)
        return self._units
    
    @property
    def vehicles(self) -> vehicle_repository_base.VehicleRepositoryBase:
        if self._vehicles is None:
            self._vehicles = vehicle_repository.VehicleRepository(self.db)
        return self._vehicles
    
    @property
    def stores(self) -> store_repository_base.StoreRepositoryBase:
        if self._stores is None:
            self._stores = store_repository.StoreRepository(self.db)
        return self._stores
    
    def refresh(self, entity):
        self.db.refresh(entity)
    
    def commit(self):
        self.db.commit()
        
    def rollback(self):
        self.db.rollback()