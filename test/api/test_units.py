from fastapi.testclient import TestClient

from fastapi import status

from sqlalchemy.orm import Session

from test.utils.unit_randomizer import create_random_unit_data
from test.utils.vehicle_randomizer import create_random_vehicle_data


# def test_create_unit(client: TestClient, db: Session) -> None:
#     """
#     GIVEN a FastAPI application
#     WHEN the POST endpoint '/api/v1/units/' is requested
#     THEN check that the response is valid
#     """
#     for i in range(500):
#         random_unit = create_random_unit_data()
#         random_vehicle = create_random_vehicle_data()
#         response = client.post("/api/v1/units/", json={"unit": random_unit, "vehicle": random_vehicle})
#         assert response.status_code == status.HTTP_201_CREATED
