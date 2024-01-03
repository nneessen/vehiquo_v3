from fastapi.testclient import TestClient

from ..database_test import configure_test_database, clear_database

from ..base_insertion import insert_into_users

from ..templates.user_templates import user_json, user_not_found_error

from app.main import get_application


client = TestClient(get_application())

users_route = "/api/v1/users"


def setup_module(module):
    configure_test_database(get_application())


def setup_function(module):
    clear_database()
    

def test_create_user(user_json):
    ''' Create a user with success '''
    response = client.post(users_route + "/", json=user_json)
    assert response.status_code == 201
    assert response.json() == user_json


def test_read_user(user_json):
    ''' Read a user with success '''
    insert_into_users(user_json)
    request_url = users_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == user_json


def test_read_users(user_json):
    ''' Read all users paginated with success '''
    insert_into_users(user_json)
    request_url = users_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [ user_json ]


def test_delete_user(user_json):
    ''' Delete a user with success '''
    insert_into_users(user_json)
    request_url = users_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_user_not_found(user_not_found_error):
    ''' Read a user when not found '''
    request_url = users_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == user_not_found_error
    
    
def test_read_users_not_found():
    ''' Read all users paginated when not found '''
    request_url = users_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_user_not_found(user_not_found_error):
    ''' Delete a user when not exists '''
    request_url = users_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == user_not_found_error
    