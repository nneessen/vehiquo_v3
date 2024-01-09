from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.unit_of_work.unit_of_work import UnitOfWork

from app.schemas import stores as stores_schema
from app.schemas import users as users_schema
from app.schemas import units as units_schema
from app.schemas import vehicles as vehicles_schema

from app.services import stores as store_service
from app.services import users as user_service
from app.services import units as unit_service
from app.services import vehicles as vehicle_service

from app.routers.users import get_current_user


router = APIRouter(prefix="/stores", tags=["Stores"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=stores_schema.StoreOutput)
def create_store(store: stores_schema.StoreAdd, db: Session = Depends(get_db)) -> stores_schema.StoreOutput:
    db_store = store_service.create_store(db, store=store)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return {"Status": "Success", "Store": db_store}


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[stores_schema.StoreOutput])
def get_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[stores_schema.StoreOutput]:
    stores = store_service.get_stores(db, skip=skip, limit=limit)
    return {"Status": "Success", "Stores": stores}


@router.get("/{store_id}", status_code=status.HTTP_200_OK, response_model=stores_schema.StoreOutput)
def get_store(store_id: int, db: Session = Depends(get_db)) -> stores_schema.StoreOutput:
    store = store_service.get_store_by_id(db, store_id=store_id)
    if not store:
        raise HTTPException(
            status_code=404, 
            detail=f"Store with id {store_id} not found"
            )
    return {"Status": "Success", "Store": store}


@router.delete("/{store_id}", response_model=stores_schema.StoreOutput)
def delete_store(store_id: int, db: Session = Depends(get_db)) -> stores_schema.StoreOutput:
    with UnitOfWork(db) as uow:
        try:
            db_store = store_service.delete_store(db, store_id=store_id)
            if db_store is None:
                raise HTTPException(status_code=404, detail="Store not found")
            return {"Status": "Success", "Store": db_store}
        except Exception as e:
            uow.rollback()
            raise e


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