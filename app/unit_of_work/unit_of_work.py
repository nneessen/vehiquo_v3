from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import select, and_


from app.repositories.user_repository import UserRepositoryBase, UserRepository



class UnitOfWorkBase(ABC):
    users: UserRepositoryBase
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.rollback()
        
    @abstractmethod
    def commit(self):
        raise NotImplementedError()
    
    @abstractmethod
    def rollback(self):
        raise NotImplementedError()
    

class UnitOfWork(UnitOfWorkBase):
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def __enter__(self):
        self.db = Session()
        self.users = UserRepository(self.db)
        return super().__enter__()
    
    def commit(self):
        self.db.commit()
        
    def rollback(self):
        self.db.rollback()