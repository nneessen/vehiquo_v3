from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Type, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, update, delete, insert, exists, func
from app.repositories.base.sql_repository_base import SqlRepositoryBase

T = TypeVar("T")

class SqlRepository(SqlRepositoryBase[T], ABC):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def _add(self, entity: T) -> T:
        self.model = self.model(**entity.__dict__)
        self.db.add(self.model)
        self.db.commit()
        self.db.refresh(self.model)
        return self.model
    
  