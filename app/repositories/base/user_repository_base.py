from abc import ABC, abstractmethod

from typing import Optional, List

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
    def get_users(self, skip: int, limit: int) -> List[User]:
        raise NotImplementedError()
    
    @abstractmethod
    def update_user(self, user_id: int, user: User) -> User:
        raise NotImplementedError()
    