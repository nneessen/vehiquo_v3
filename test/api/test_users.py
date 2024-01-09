from typing import Dict

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.schemas.users import UserCreate
from app.services.users import get_user_by_email, create_user, get_user_by_username, get_user
from test.utils.data_randomizer import random_user_create, create_me



    
def create_me_as_admin(client: TestClient, db: Session) -> None:
    me = create_me()
    user_in = dict(UserCreate(**me))
    r = client.post("/api/v1/users/", json=user_in)
    assert 200 <= r.status_code < 300


def test_create_user(client: TestClient, db: Session) -> None:
    """
    GIVEN a FastAPI application
    WHEN the POST endpoint '/api/v1/users/' is requested
    THEN check that the response is valid
    """
    random_user_data = random_user_create()
    user_in = dict(UserCreate(**random_user_data))
    r = client.post("/api/v1/users/", json=user_in)
    assert 200 <= r.status_code < 300
    user_data = r.json()
    user = get_user_by_username(db, user_data["username"])
    user.store_id = 1
    db.commit()
    db.refresh(user)
    assert user_data["email"] == user_in["email"]
    assert user.store_id == 1
    

def test_create_user_with_existing_email(client: TestClient, db: Session) -> None:
    """
    GIVEN a FastAPI application
    WHEN the POST endpoint '/api/v1/users/' is requested and email already exists
    THEN check that the response is valid
    """
    user_data = {
        "first_name": "Nick",
        "last_name": "Neessen",
        "email": "elqsqdstqsjqjajirnqtpqbxy@nsnisnpkztolnsikawejjindp.com",
        "username": "abzrpjjdblejwldnmtyazyfmx",
        "password": "password",
        "phone_number": "8594335907",
    }
    user_in = dict(UserCreate(**user_data))
    r = client.post("/api/v1/users/", json=user_in)
    assert r.status_code == status.HTTP_400_BAD_REQUEST