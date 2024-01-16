from abc import ABC, abstractmethod

from typing import Optional, List, Any

from app.repositories.sql_repository import SqlRepository

from app.models.users import User



class UserRepositoryBase(SqlRepository[User], ABC):

    @abstractmethod
    def add_user(self, user: User) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_users(self, 
        skip: int, 
        limit: int,
        filter: Optional[dict] = None,
        to_join: bool = False,
        model_to_join: Optional[str] = None,
        joined_model_filters: Optional[dict] = None
        ) -> List[User]:
        raise NotImplementedError()
    
    @abstractmethod
    def update_user(self, user_id: int, user: User) -> User:
        raise NotImplementedError()
    