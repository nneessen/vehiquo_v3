from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.users import UserCreate
from app.services.users import get_user_by_email, create_user, get_user_by_username
from test.utils.data_randomizer import random_lower_string, random_email, random_phone_number




def test_create_user(client: TestClient, db: Session) -> None:
    """
    GIVEN a FastAPI application
    WHEN the POST endpoint '/api/v1/users/' is requested
    THEN check that the response is valid
    """
    first_name = random_lower_string()
    last_name = random_lower_string()
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    phone_number = random_phone_number()
    user_in = UserCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password=password,
        phone_number=phone_number,
    )
    user = create_user(db, user_in)
    assert user
    user_out = get_user_by_email(db, email)
    assert user_out
    assert user_out.email == email
    

def test_create_user_existing_username(client: TestClient, db: Session) -> None:
    """
    GIVEN a FastAPI application
    WHEN the POST endpoint '/api/v1/users/' is requested with an existing username
    THEN check that the response is valid
    """
    first_name = random_lower_string()
    last_name = random_lower_string()
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    phone_number = random_phone_number()
    user_in = UserCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password=password,
        phone_number=phone_number,
    )
    user = create_user(db, user_in)
    r = client.post("/api/v1/users/", json=user_in)
    assert r.status_code == 400
    assert r.json()["detail"] == "Username already registered"
    
