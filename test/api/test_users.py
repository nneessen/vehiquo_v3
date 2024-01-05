from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.users import UserCreate
from app.services.users import get_user_by_email, create_user, get_user_by_username
from test.utils.data_randomizer import random_user_data, create_me




def test_create_user(client: TestClient, db: Session) -> None:
    """
    GIVEN a FastAPI application
    WHEN the POST endpoint '/api/v1/users/' is requested
    THEN check that the response is valid
    """
    user_in = dict(UserCreate(**random_user_data))
    r = client.post("/api/v1/users/", json=user_in)
    assert 200 <= r.status_code < 300
    user_data = r.json()
    assert user_data["email"] == user_in["email"]