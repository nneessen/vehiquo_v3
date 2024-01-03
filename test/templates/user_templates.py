import pytest


@pytest.fixture
def user_json():
    return {
        "id": 1,
        "first_name": "Nick",
        "last_name": "Neessen",
        "email": "nick.neessen@gmail.com",
        "password": "password",
    }


@pytest.fixture
def user_not_found_error():
    return { 'errors': ['user does not exist'] }
