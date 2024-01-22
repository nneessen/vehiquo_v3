from fastapi.testclient import TestClient

from fastapi import status

from sqlalchemy.orm import Session

from app.schemas.users import UserLogin

from test.utils.unit_randomizer import create_random_unit_data
from test.utils.vehicle_randomizer import create_random_vehicle_data

from app.routers.security.dependencies import CURRENT_USER


# def test_create_unit(client: TestClient, db: Session) -> None:
#     """
#     GIVEN a FastAPI application
#     WHEN the POST endpoint '/api/v1/units/' VERIFY that the current user is an admin
#     THEN check that the response is valid
#     """
#     admin_creds = {"username": "admin", "password": "password"}
#     user_in = dict(UserLogin(**admin_creds))
#     response = client.post("/api/v1/token/", data=user_in)
#     assert response.status_code == status.HTTP_200_OK
#     access_token = response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {access_token}"}
    
#     for i in range(500):
#         random_unit = create_random_unit_data()
#         random_vehicle = create_random_vehicle_data()
#         response = client.post("/api/v1/units/", headers=headers, json={"unit": random_unit, "vehicle": random_vehicle})
#         assert response.status_code == status.HTTP_201_CREATED
        