from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.users import UserCreate


def test_create_user(client: TestClient, db: Session) -> None:
    data = {
        "first_name": "melani",
        "last_name": "lighter",
        "email": "melanilighter@gmail.com",
        "username": "melanilighter",
        "password": "password",
        "phone_number": "6519816512",
    }
    r = client.post("/api/v1/users/", json=data)
    assert r.status_code == 201
    


    