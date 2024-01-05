from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from app.sql_repository import SqlRepository
from app.models import User



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
    def add(self, user: User) -> User:
        raise NotImplementedError()
    

class UserRepository(UserRepositoryBase, SqlRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, User)
        
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()