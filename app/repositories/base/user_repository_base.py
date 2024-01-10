from abc import ABC, abstractmethod

from typing import Optional, List

from app.repositories.sql_repository import SqlRepository

from app.models.users import User



class UserRepositoryBase(SqlRepository[User], ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError()
    
    @abstractmethod
    def list(self, skip: int, limit: int) -> List[User]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, id: int, user: User) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    def confirm(self, user: User) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    def get(self, id: int) -> Optional[User]:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all(self) -> List[User]:
        raise NotImplementedError()
    
    @abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError()