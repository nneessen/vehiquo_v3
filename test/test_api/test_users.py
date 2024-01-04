from fastapi.testclient import TestClient

from ..database_test import configure_test_database, clear_database

from ..base_insertion import insert_into_users

from ..templates.user_templates import user_json, user_not_found_error

from app.main import get_application

client = TestClient(get_application())



def setup_module(module):
    configure_test_database(get_application())


def setup_function(module):
    clear_database()
    

def test_create_user(user_json):
    payload = user_json
    response = client.post("/api/users/", json=payload)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "first_name": "Nick",
        "last_name": "Neessen",
        "email": "nick.neessen@gmail.com",
        "username": "nickneessen",
        "phone_number": "8594335907",
        "confirmed": False,
        "twilio_opt_in": False,
        "is_blocked": False,
        "is_active": False,
        "is_buyer": False,
        "is_admin": False,
        "is_superuser": False,
    }