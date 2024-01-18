from typing import Optional, List, Any, Annotated, Union, Literal

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.unit_of_work.unit_of_work import UnitOfWork

from app.schemas import stores as stores_schema
from app.schemas import units as units_schema

from app.services import stores as store_service
from app.services import units as unit_service

from app.utils.mapper import map_string_to_model


router = APIRouter(prefix="/stores", tags=["Stores"])

StoreResponseModel = Annotated[stores_schema.StoreOutput, Literal["StoreResponseModel"]]


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=stores_schema.StoreOutput
)
def create_store(
    store: stores_schema.StoreCreate, 
    db: Session = Depends(get_db)) -> stores_schema.StoreOutput:

    db_store = store_service.create_store(db, store=store)

    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@router.delete("/{store_id}", response_model=None)
def delete_store(store_id: int, db: Session = Depends(get_db)) -> Optional[stores_schema.StoreOutput]:
    db_store = store_service.get_store_by_id(db, store_id)
    if not db_store:
        return {"Status": "Failure", "Message": f"Store with {store_id} does not exist"}
    store_service.delete_store(db, store_id)
    return {"Status": "Success", "Message": f"Store with {store_id} has bee successfully deleted!"}
    

@router.get("/{store_id}", status_code=status.HTTP_200_OK, response_model=stores_schema.StoreOutput)
def get_store(store_id: int, db: Session = Depends(get_db)) -> stores_schema.StoreOutput:
    store = store_service.get_store_by_id(db, store_id=store_id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Store with id {store_id} not found"
            )
    return store


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[StoreResponseModel])
def get_stores(db: Session = Depends(get_db),
               skip: int = 0, 
               limit: int = 100,
               filter_key: Optional[str] = None,
               filter_value: Optional[str] = None,
               to_join: bool = False,
               model_to_join: Optional[str] = None,
               joined_model_filter_key: Optional[str] = None,
               joined_model_filter_value: Optional[str] = None
    ) -> StoreResponseModel:
    
    filter = {filter_key: filter_value} if filter_key and filter_value else None
    joined_model_filters = {joined_model_filter_key: joined_model_filter_value} if joined_model_filter_key and joined_model_filter_value else None

    if model_to_join:
        model_to_join = map_string_to_model(model_to_join)
        
    stores = store_service.get_stores(
        db, 
        skip=skip, 
        limit=limit, 
        filter=filter, 
        to_join=to_join, 
        model_to_join=model_to_join, 
        joined_model_filters=joined_model_filters
    )
    
    if not stores:
        raise HTTPException(
            status_code=404, 
            detail=f"Stores not found"
            )
    return stores








@router.put("/{store_id}", response_model=stores_schema.StoreOutput)
def update_store(store_id: int, store: stores_schema.StoreUpdate, db: Session = Depends(get_db)) -> stores_schema.StoreOutput:
    with UnitOfWork(db) as uow:
        try:
            db_store = store_service.update_store(db, store_id=store_id, store=store)
            if db_store is None:
                raise HTTPException(status_code=404, detail="Store not found")
            return {"Status": "Success", "Store": db_store}
        except Exception as e:
            uow.rollback()
            raise e


@router.get("/{store_id}/units", status_code=status.HTTP_200_OK, response_model=list[units_schema.UnitOutput])
def get_store_units(store_id: int, db: Session = Depends(get_db)) -> list[units_schema.UnitOutput]:
    units = unit_service.get_store_units(db, store_id=store_id)
    return {"Status": "Success", "Units": units}