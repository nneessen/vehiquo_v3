import random
import string
from typing import Dict

from fastapi.testclient import TestClient


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=25))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_phone_number() -> str:
    return f"{random.randint(1000000000, 9999999999)}"


def random_user_create() -> Dict:
    return {
        "first_name": random_lower_string(),
        "last_name": random_lower_string(),
        "email": random_email(),
        "username": random_lower_string(),
        "password": random_lower_string(),
        "phone_number": random_phone_number(),
    }
    
