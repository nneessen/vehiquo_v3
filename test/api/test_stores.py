from typing import Dict

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.schemas.stores import StoreUpdate, StoreDelete, StoreOutput, StoreAdd
from app.schemas.users import UserLogin

from app.services.stores import create_store, get_store_by_id

from test.utils.store_randomizer import random_store_create

#✅
def test_create_store(client: TestClient, db: Session) -> None:
    creds = {"username": "admin", "password": "password"}
    user_in = dict(UserLogin(**creds))
    response = client.post("/api/v1/token/", data=user_in)
    assert response.status_code == status.HTTP_200_OK
    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    for i in range(25):
        random_store = random_store_create()
        store_in = dict(StoreAdd(**random_store))
        r = client.post("/api/v1/stores/", headers=headers, json=store_in)
        assert 200 <= r.status_code < 300


#✅
# def test_create_store_with_duplicate_store_name_should_fail(client: TestClient, db: Session) -> None:
#     """
#     GIVEN a FastAPI application
#     WHEN the POST endpoint '/api/v1/stores/' is requested and store name already exists
#     THEN check that the response is valid
#     """
#     store_data = {
#         "name": "Test Store",
#         "street_address": "123 Main St",
#         "city": "Lexington",
#         "state": "KY",
#         "zip_code": 40517,
#         "phone": "8595555555",
#         "admin_clerk_1": "John Doe",
#         "is_primary_hub": True,
#         "qb_customer_id": 123456,
#     }
#     r = client.post("/api/v1/stores/", json=store_data)
#     assert 409 == r.status_code