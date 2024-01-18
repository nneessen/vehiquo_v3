from typing import Dict, List, Optional

from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy.orm import Session

from app.schemas.units import UnitAdd, UnitUpdate, UnitOutput
from app.schemas.vehicles import VehicleAdd, VehicleOutput

from app.services.units import create_unit, get_unit_by_id, get_units, get_store_units
from app.services.vehicles import create_vehicle, get_vehicle_by_id, get_vehicles

from test.utils.unit_randomizer import create_random_unit_data
from test.utils.vehicle_randomizer import create_random_vehicle_data


def test_create_unit(client: TestClient, db: Session) -> None:
    """
    GIVEN a FastAPI application
    WHEN the POST endpoint '/api/v1/units/' is requested
    THEN check that the response is valid
    """
    for i in range(100):
        random_unit = create_random_unit_data()
        random_vehicle = create_random_vehicle_data()
        response = client.post("/api/v1/units/", json={"unit": random_unit, "vehicle": random_vehicle})
        assert response.status_code == status.HTTP_201_CREATED
