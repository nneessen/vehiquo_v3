import random
from faker import Faker
from typing import Dict





def random_user_create() -> Dict:
    faker = Faker("en_US")
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "username": faker.user_name(),
        "password": "password",
        "phone_number": faker.phone_number(),
        "is_admin": 0,
        "is_superuser": 0,
        "is_active": 1,
        "store_id": random.randint(2, 25),
    }

def create_admin() -> Dict:
    return {
        "first_name": "Nick",
        "last_name": "Neessen",
        "email": "nick.neessen@gmail.com",
        "username": "admin",
        "password": "password",
        "phone_number": "8594335907",
        "is_admin": 1,
        "is_superuser": 1,
        "is_active": 1,
        "store_id": 1,
    }

