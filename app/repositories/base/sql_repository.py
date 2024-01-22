from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import and_, delete, exists, func, insert, select, update
from sqlalchemy.orm import Session, joinedload, selectinload

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
            return Session.get(self.db, self.model, inserted_id)
        except Exception as e:
            self.db.rollback()
            raise e

    def _delete(self, entity_id: int):
        try:
            stmt = delete(self.model).where(self.model.id == entity_id)
            self.db.execute(stmt)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    #
    def _get(self, entity_id: int) -> Optional[T]:
        try:
            stmt = select(self.model).where(self.model.id == entity_id)
            entity = self.db.execute(stmt).scalar()
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    def _get_all(
        self,
        skip: int,
        limit: int,
        filter: Optional[dict] = None,
        to_join: bool = False,
        models_to_join: Optional[List[T]] = None,  # List of model classes
        joined_model_filters: Optional[dict] = None,
    ) -> List[T]:
        try:
            stmt = select(self.model).offset(skip).limit(limit)

            # Apply filters if provided - filter only applies to the main model
            if filter:
                stmt = stmt.filter_by(**filter)

            # Control the loading of related entities
            if to_join and models_to_join:
                for model in models_to_join:
                    stmt = stmt.join(model)
                    if joined_model_filters:
                        stmt = stmt.filter_by(**joined_model_filters)
            else:
                for relationship in self.model.__mapper__.relationships:
                    # use class-bound attribute instead of string or error occurs
                    relationship_attr = getattr(self.model, relationship.key)
                    stmt = stmt.options(selectinload(relationship_attr))

            entities = self.db.execute(stmt).scalars().all()
            return entities
        except Exception as e:
            self.db.rollback()
            raise e

    def _update(self, entity: T, entity_id: int) -> T:
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == entity_id)
                .values(**entity.__dict__)
            )
            self.db.execute(stmt)
            self.db.commit()
            return self.db.query(self.model).get(entity_id)
        except Exception as e:
            self.db.rollback()
            raise e
