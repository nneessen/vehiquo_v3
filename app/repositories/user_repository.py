from typing import Optional, List

from sqlalchemy.orm import Session

from app.repositories.sql_repository import SqlRepository

from app.models.users import User

from app.repositories.base.user_repository_base import UserRepositoryBase

    

class UserRepository(UserRepositoryBase, SqlRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, User)
        
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def list(self, skip: int, limit: int) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def delete(self, id: int) -> None:
        self.db.query(User).filter(User.id == id).delete()
        
    def update(self, id: int, user: User) -> User:
        self.db.query(User).filter(User.id == id).update(user)
        return user
    
    def confirm(self, user: User) -> User:
        user.confirmed = True
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get(self, id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()
    
    def get_all(self) -> List[User]:
        return super().get_all()
    
    
    def add(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user