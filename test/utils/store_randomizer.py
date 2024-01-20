import random

from typing import Dict

from faker import Faker


def create_random_store_name() -> str:
    fake = Faker()
    return fake.company()

def create_random_street_address() -> str:
    fake = Faker()
    return fake.street_address()

def create_random_city() -> str:
    fake = Faker()
    return fake.city()

def create_random_state() -> str:
    fake = Faker()
    return fake.state_abbr()

def create_random_zip_code() -> str:
    fake = Faker()
    return fake.zipcode()

def create_random_store_phone_number() -> str:
    fake = Faker("en_US")
    return fake.phone_number()

def random_store_create() -> Dict:
    return {
        "name": create_random_store_name(),
        "street_address": create_random_street_address(),
        "city": create_random_city(),
        "state": create_random_state(),
        "zip_code": create_random_zip_code(),
        "phone": create_random_store_phone_number(),
        "admin_clerk_1": "N/A",
        "is_primary_hub": False,
        "qb_customer_id": random.randint(1, 1000000)
    }