from typing import Optional, List, Any

from sqlalchemy.orm import Session

from app.repositories.base.sql_repository import SqlRepository

from app.repositories.stores.store_repository_base import StoreRepositoryBase

from app.models.stores import Store
from app.models.units import Unit
from app.models.vehicles import Vehicle
from app.models.users import User

from app.exceptions.custom_exceptions import (
    DeleteStoreException,
    AddStoreException,
    UpdateStoreException, 
    GetStoreException
)