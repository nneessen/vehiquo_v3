import random
import string
from typing import Dict



def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=25))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_phone_number() -> str:
    return f"{random.randint(1000000000, 9999999999)}"


def random_password() -> str:
    return random_lower_string()





def random_user_create() -> Dict:
    return {
        "first_name": random_lower_string(),
        "last_name": random_lower_string(),
        "email": random_email(),
        "username": random_lower_string(),
        "password": random_lower_string(),
        "phone_number": random_phone_number(),
    }
     
random_user_data = random_user_create()


def create_me() -> Dict:
    return {
        "first_name": "Nick",
        "last_name": "Neessen",
        "email": "nick.neessen@gmail.com",
        "username": "nneessen",
        "password": "password",
        "phone_number": "8594335907",
        "is_admin": True,
    }

