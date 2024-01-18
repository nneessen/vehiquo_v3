from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional


T = TypeVar("T")

class SqlRepositoryBase(Generic[T], ABC):

    @abstractmethod
    def _add(self, entity: T) -> T:
        raise NotImplementedError()
    
    @abstractmethod
    def _delete(self, entity_id: int):
        raise NotImplementedError()
    
    @abstractmethod
    def _get(self, entity_id: int) -> Optional[T]:
        raise NotImplementedError()
    
    @abstractmethod
    def _get_all(self, 
        skip: int, 
        limit: int, 
        filter: Optional[dict] = None, 
        to_join: bool = False, 
        models_to_join: Optional[List[T]] = None,
        joined_model_filters: Optional[dict] = None
        ) -> List[T]:
        """
        This method is used to get all rows from a table in the database with the option to apply filters and joins
        
        Args:
            skip (int): Number of rows to skip
            limit (int): Maximum number of rows to return
            filter (Optional[dict], optional): Dictionary of filters to apply. Defaults to None.
            to_join (bool, optional): Whether to join another table. Defaults to False.
            models_to_join (Optional[List[T]], optional): The model to join. Defaults to None.
            joined_model_filters (Optional[dict], optional): Filters to apply to the joined table. Defaults to None.
        Returns:
            List[T]: A list of rows from the database
        """
        raise NotImplementedError()
    
    @abstractmethod
    def _update(self, entity: T, entity_id: int) -> T:
        raise NotImplementedError()