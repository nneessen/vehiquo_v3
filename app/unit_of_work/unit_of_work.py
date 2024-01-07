import logging

from abc import ABC, abstractmethod
from typing import Callable
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.logging_config import setup_logging
from app.repositories.user_repository import UserRepositoryBase, UserRepository


setup_logging()
logger = logging.getLogger(__name__)


class UnitOfWorkBase(ABC):
    users: UserRepositoryBase
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logger.error(f"Error: {exc_value}")
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
        return super().__enter__()
    
    def commit(self):
        self.db.commit()
        
    def rollback(self):
        self.db.rollback()