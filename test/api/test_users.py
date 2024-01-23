from typing import Dict

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.schemas.users import (
    UserLogin,
    UserCreate,
    UserInDB
    )
from test.utils.user_randomizer import random_user_create, create_admin

#✅
# def test_create_admin(client: TestClient, db: Session) -> None:
#     admin_user_data = create_admin()
#     user_in = dict(UserCreate(**admin_user_data))
#     r = client.post("/api/v1/users/", json=user_in)
#     assert r.status_code == 400


#✅
# def test_create_users(client: TestClient, db: Session) -> None:
#     creds = {"username": "admin", "password": "password"}
#     user_in = dict(UserLogin(**creds))
#     response = client.post("/api/v1/token", data=user_in)
#     assert response.status_code == status.HTTP_200_OK
#     assert "access_token" in response.json()
#     assert response.json()["token_type"] == "bearer"
#     access_token = response.json()['access_token']
#     for i in range(49):
#         random_user_data = random_user_create()
#         user_in = dict(UserCreate(**random_user_data))
#         r = client.post("/api/v1/users/", headers={"Authorization": f"Bearer {access_token}"}, json=user_in)
#         assert 200 <= r.status_code < 300


#✅
# def test_login(client: TestClient, db: Session) -> None:
#     user_data = {
#         "username": "admin",
#         "password": "password",
#     }
#     user_in = dict(UserLogin(**user_data))
#     r = client.post("/api/v1/token", data=user_in)
#     assert r.status_code == status.HTTP_200_OK
#     assert "access_token" in r.json()
#     assert r.json()["token_type"] == "bearer"


# def create_token(client: TestClient, username: str, password: str) -> Dict[str, str]:
#     user_data = {
#         "username": username,
#         "password": password,
#     }
#     user_in = dict(UserLogin(**user_data))
#     r = client.post("/api/v1/token", data=user_in)
#     return r.json()['access_token']


# def test_delete_user_with_admin_user(db: Session, client: TestClient) -> None:
#     admin_token = create_token(client, "admin", "password")
#     r = client.delete("/api/v1/users/4", headers={"Authorization": f"Bearer {admin_token}"})
#     assert r.status_code == status.HTTP_200_OK


#✅
# def test_create_user_with_existing_email(client: TestClient) -> None:
#     """
#     GIVEN a FastAPI application
#     WHEN the POST endpoint '/api/v1/users/' is requested and email already exists
#     THEN check that the response is valid
#     """
#     user_data = {
#         "first_name": "Nick",
#         "last_name": "Neessen",
#         "email": "nick.neessen@gmail.com",
#         "username": "admin",
#         "password": "password",
#         "phone_number": "8594335907",
#     }
#     user_in = dict(UserCreate(**user_data))
#     r = client.post("/api/v1/users/", json=user_in)
#     assert r.status_code == status.HTTP_400_BAD_REQUEST


#✅
# def test_assign_user_to_store(db: Session) -> None:
#     user = get_user_by_username(db, "admin")
#     user.store_id = 1
#     db.commit()
#     assert user.store_id == 1
#     assert user.is_admin == True