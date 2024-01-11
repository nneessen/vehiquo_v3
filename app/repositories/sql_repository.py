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

    ########################################
    # Abstract methods to be implemented by subclasses
    ########################################
    def begin_transaction(self):
        self.db.begin()
        
    def commit_transaction(self):
        self.db.commit()
        
    def rollback_transaction(self):
        self.db.rollback()
        
    def end_transaction(self):
        self.db.close()
    
    def construct_get_stmt(self, id: int):
        return select(self.model).where(self.model.id==id)
    
    def construct_update_stmt(self, id: int, entity: T):
        return self.model.update().where(self.model.id==id).values(entity)
    
    def construct_delete_stmt(self, id: int):
        return self.model.delete().where(self.model.id==id)
    
    def construct_add_stmt(self, entity: T):
        return self.model.insert().values(entity)
    
    def construct_list_stmt(self, **filters):
        stmt = select(self.model)
        where_filters = []
        for key, value in filters.items():
            if not hasattr(self.model, key):
                raise ValueError(f"Invalid filter: {key}")
            where_filters.append(getattr(self.model, key)==value)
        if len(where_filters) == 1:
            stmt = stmt.where(where_filters[0])
        elif len(where_filters) > 1:
            stmt = stmt.where(and_(*where_filters))
        return stmt
    
    def construct_count_stmt(self, **filters):
        stmt = select(func.count(self.model.id))
        where_filters = []
        for key, value in filters.items():
            if not hasattr(self.model, key):
                raise ValueError(f"Invalid filter: {key}")
            where_filters.append(getattr(self.model, key)==value)
        if len(where_filters) == 1:
            stmt = stmt.where(where_filters[0])
        elif len(where_filters) > 1:
            stmt = stmt.where(and_(*where_filters))
        return stmt
    
    def construct_exists_stmt(self, **filters):
        stmt = exists().select_from(self.model)
        where_filters = []
        for key, value in filters.items():
            if not hasattr(self.model, key):
                raise ValueError(f"Invalid filter: {key}")
            where_filters.append(getattr(self.model, key)==value)
        if len(where_filters) == 1:
            stmt = stmt.where(where_filters[0])
        elif len(where_filters) > 1:
            stmt = stmt.where(and_(*where_filters))
        return stmt
    
    def get(self, id: int) -> Optional[T]:
        return self.db.execute(self.construct_get_stmt(id)).scalar_one_or_none()
    
    def get_all(self) -> List[T]:
        return self.db.execute(select(self.model)).scalars().all()
    
    def add(self, entity: T) -> T:
        self.db.execute(self.construct_add_stmt(entity))
        self.db.commit()
        return entity
    
    def add_all(self, entities: List[T]) -> List[T]:
        self.db.add_all(entities)
        self.db.commit()
        return entities
    
    def update(self, id: int, entity: T) -> T:
        self.db.execute(self.construct_update_stmt(id, entity))
        self.db.commit()
        return entity
    
    def delete(self, id: int) -> None:
        self.db.execute(self.construct_delete_stmt(id))
        self.db.commit()

    def list(self, **filters) -> List[T]:
        return self.db.execute(self.construct_list_stmt(**filters)).scalars().all()
    
    def count(self, **filters) -> int:
        return self.db.execute(self.construct_count_stmt(**filters)).scalar_one()
    
    def exists(self, **filters) -> bool:
        return self.db.execute(self.construct_exists_stmt(**filters)).scalar_one()