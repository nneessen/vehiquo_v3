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
        try:
            stmt = insert(self.model).values(**entity.__dict__)
            result = self.db.execute(stmt)
            self.db.commit()
            
            inserted_id = result.inserted_primary_key[0]
            return self.db.query(self.model).get(inserted_id)
        except Exception as e:
            self.db.rollback()
            raise e

    def _delete(self, entity_id: int):
        try:
            stmt = delete(self.model).where(self.model.id==entity_id)
            self.db.execute(stmt)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
#
    def _get(self, entity_id: int) -> Optional[T]:
        try:
            stmt = select(self.model).where(self.model.id==entity_id)
            entity = self.db.execute(stmt).scalar()
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    def _get_all(self, 
        skip: int, 
        limit: int, 
        filter: Optional[dict] = None,
        to_join: bool = False,
        model_to_join: Optional[T] = None,
        joined_model_filters: Optional[dict] = None
        ) -> List[T]:
        try:
            stmt = select(self.model).offset(skip).limit(limit)
            if filter:
                stmt = stmt.filter_by(**filter)
            if to_join:
                stmt = stmt.join(model_to_join)
                if joined_model_filters:
                    stmt = stmt.filter_by(**joined_model_filters)

            entities = self.db.execute(stmt).scalars().all()
            return entities
        except Exception as e:
            self.db.rollback()
            raise e



    def _update(self, entity: T, entity_id: int) -> T:
        try:
            stmt = update(self.model).where(self.model.id==entity_id).values(**entity.__dict__)
            self.db.execute(stmt)
            self.db.commit()
            return self.db.query(self.model).get(entity_id)
        except Exception as e:
            self.db.rollback()
            raise e