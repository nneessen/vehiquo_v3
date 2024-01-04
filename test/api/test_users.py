from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.schemas.users import UserCreate
from test.utils.data_randomizer import random_user_create



random_user_data = random_user_create()

def test_create_user(client: TestClient, db: Session) -> None:
    response = client.post("/api/v1/users/", json=random_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == random_user_data["email"]
    
    
    


    