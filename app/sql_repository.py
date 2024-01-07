from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Type, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_


T = TypeVar("T")

class SqlRepositoryBase(Generic[T], ABC):

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError()

    @abstractmethod
    def add(self, entity: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError()


class SqlRepository(SqlRepositoryBase[T], ABC):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def construct_get_stmt(self, id: int):
        return select(self.model).where(self.model.id==id)
    
    def get(self, id: int) -> Optional[T]:
        return self.db.execute(self.construct_get_stmt(id)).scalar_one_or_none()

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
    
    def list(self, **filters) -> List[T]:
        return self.db.execute(self.construct_list_stmt(**filters)).scalars().all()
    
    def add(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def update(self, entity: T) -> T:
        self.db.add(entity)
        self.db.flush()
        self.db.refresh(entity)
        return entity
    
    def delete(self, id: int) -> None:
        entity = self.get(id)
        if entity is not None:
            self.db.delete(entity)
            self.db.flush()