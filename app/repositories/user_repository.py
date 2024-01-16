from typing import Optional, List

from sqlalchemy.orm import Session

from app.repositories.sql_repository import SqlRepository

from app.models.users import User

from app.repositories.base.user_repository_base import UserRepositoryBase

from app.exceptions.custom_exceptions import (
    AddUserException, 
    DeleteUserException,
    UpdateUserException,
    GetUserException
)


class UserRepository(UserRepositoryBase, SqlRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, User)

    def add_user(self, user: User) -> User:
        try:
            return super()._add(user)
        except Exception as e:
            message = f"Error adding {user}"
            error_code = "user_add_error"
            raise AddUserException(message, error_code)

    def delete_user(self, user_id: int) -> User:
        try:
            return super()._delete(user_id)
        except Exception as e:
            message = f"Error occured while deleting user with id {user_id}"
            error_code = "UserRepository.delete_user error"
            raise DeleteUserException(message, error_code)

    def get_user(self, user_id: int) -> Optional[User]:
        try:
            return super()._get(user_id)
        except Exception as e:
            message = f"Error getting user with id {user_id}"
            error_code = "user_get_error"
            raise GetUserException(message, error_code)

    def get_users(self, skip: int, limit: int) -> List[User]:
        try:
            return super()._get_all(skip, limit)
        except Exception as e:
            message = f"Error getting users"
            error_code = "user_get_all_error"
            raise GetUserException(message, error_code)
    
    def update_user(self, user: User, user_id: int) -> User:
        try:
            return super()._update(user, user_id)
        except Exception as e:
            message = f"Error updating user with id {user.id}"
            error_code = "user_update_error"
            raise UpdateUserException(message, error_code)
