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

from app.routers.security.dependencies import CURRENT_USER, SESSION

router = APIRouter(prefix="/stores", tags=["Stores"])

StoreResponseModel = Annotated[stores_schema.StoreOutput, Literal["Default Store Response Model"]]

#✅
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=StoreResponseModel)
def create_store(
    current_user: CURRENT_USER,
    store: stores_schema.StoreAdd, 
    db: SESSION) -> StoreResponseModel:
    if not current_user.is_admin:
        raise HTTPException(status_code=401, detail="Admin access required")

    db_store = store_service.create_store(db, store=store)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store


@router.delete("/{store_id}", response_model=Optional[StoreResponseModel])
def delete_store(current_user: CURRENT_USER, store_id: int, db: SESSION) -> Optional[StoreResponseModel]:
    if not current_user.is_admin:
        return HTTPException(status_code=401, detail="Admin access required")

    db_store = store_service.get_store_by_id(db, store_id)
    if not db_store:
        return {"Status": "Failure", "Message": f"Store with {store_id} does not exist"}
    store_service.delete_store(db, store_id)
    return {"Status": "Success", "Message": f"Store with {store_id} has bee successfully deleted!"}


@router.get("/{store_id}", status_code=status.HTTP_200_OK, response_model=StoreResponseModel)
def get_store(current_user: CURRENT_USER, store_id: int, db: SESSION) -> StoreResponseModel:
    if current_user.is_active:
        store = store_service.get_store_by_id(db, store_id=store_id)
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Store with id {store_id} not found"
                )
        return store
    return HTTPException(status_code=401, detail="Inactive user")


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[StoreResponseModel])
def get_stores(
    current_user: CURRENT_USER,
    db: SESSION,
    skip: int = 0,
    limit: int = 100,
    filter_key: Optional[str] = None,
    filter_value: Optional[str] = None,
    to_join: bool = False,
    models_to_join: Optional[str] = None, # comma separated string of models to join
    joined_model_filter_key: Optional[str] = None,
    joined_model_filter_value: Optional[str] = None
) -> List[StoreResponseModel]:
    if current_user.is_active:
        filter = {filter_key: filter_value} if filter_key and filter_value else None
        joined_model_filters = {joined_model_filter_key: joined_model_filter_value} if joined_model_filter_key and joined_model_filter_value else None
        models_to_join_classes = []
        if models_to_join:
            models_to_join_classes = [map_string_to_model(model) for model in models_to_join.split(",")]
        stores = store_service.get_stores(
            db, 
            skip=skip, 
            limit=limit, 
            filter=filter, 
            to_join=to_join, 
            models_to_join=models_to_join_classes, 
            joined_model_filters=joined_model_filters
        )
        if not stores:
            raise HTTPException(
                status_code=404, 
                detail=f"Stores not found"
                )
        return stores
    return HTTPException(status_code=401, detail="Inactive user")


@router.put("/{store_id}", response_model=StoreResponseModel)
def update_store(current_user: CURRENT_USER, store_id: int, store: stores_schema.StoreUpdate, db: SESSION) -> StoreResponseModel:
    if current_user.is_active:
        db_store = store_service.update_store(db, store_id=store_id, store=store)
        if db_store is None:
            raise HTTPException(status_code=404, detail="Store not found")
        return {"Status": "Success", "Store": db_store}
    raise HTTPException(status_code=401, detail="Inactive user")
