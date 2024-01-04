import pytest


@pytest.fixture
def user_json():
    return {
        "first_name": "Nick",
        "last_name": "Neessen",
        "email": "nick.neessen@gmail.com",
        "username": "nickneessen",
        "phone_number": "8594335907",
        "password": "password",
    }


@pytest.fixture
def user_not_found_error():
    return { 'errors': ['user does not exist'] }
