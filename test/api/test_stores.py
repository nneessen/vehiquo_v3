from typing import Dict

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.schemas.stores import StoreUpdate, StoreDelete, StoreOutput, Store
from app.services.stores import create_store, get_store_by_id


def test_create_store(client: TestClient, db: Session) -> None:
    """
    GIVEN a FastAPI application
    WHEN the POST endpoint '/api/v1/stores/' is requested
    THEN check that the response is valid
    """
    store_data = {
        "name": "Test Store 2",
        "street_address": "123 Main St",
        "city": "Lexington",
        "state": "KY",
        "zip_code": 40517,
        "phone": "8595555555",
        "admin_clerk_1": "John Doe",
        "is_primary_hub": True,
        "qb_customer_id": 123456,
    }
    r = client.post("/api/v1/stores/", json=store_data)
    assert 200 <= r.status_code < 300
    store_data = r.json()
    assert store_data["name"] == store_data["name"]


def test_create_store_with_duplicate_store_name(client: TestClient, db: Session) -> None:
    """
    GIVEN a FastAPI application
    WHEN the POST endpoint '/api/v1/stores/' is requested and store name already exists
    THEN check that the response is valid
    """
    store_data = {
        "name": "Test Store",
        "street_address": "123 Main St",
        "city": "Lexington",
        "state": "KY",
        "zip_code": 40517,
        "phone": "8595555555",
        "admin_clerk_1": "John Doe",
        "is_primary_hub": True,
        "qb_customer_id": 123456,
    }
    r = client.post("/api/v1/stores/", json=store_data)
    assert 409 == r.status_code