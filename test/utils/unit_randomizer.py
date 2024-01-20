import random
import string
from typing import Dict
from datetime import datetime, timedelta


def random_buy_now_price() -> int:
    return random.randint(1000, 100000)

def random_zip_code() -> int:
    return random.randint(10000, 99999)

def random_stock_number() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=6))

def random_transportation_fee() -> int:
    return random.randint(100, 1000)

def random_transportation_distance() -> int:
    return random.randint(100, 1000)

def random_transport_company() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=6))

def create_random_unit_data() -> Dict:
    return {
        "added_by": 2,
        "list_date": datetime.utcnow().isoformat(),
        "expire_date": (datetime.utcnow() + timedelta(minutes=5)).isoformat(),
        "stock_number": random_stock_number(),
        "buy_now_price": random_buy_now_price(),
        "zip_code_loc": random_zip_code(),
        "transportation_fee": random_transportation_fee(),
        "transportation_distance": random_transportation_distance(),
        "transport_company": random_transport_company(),
        "store_id": random.randint(2, 25),
    }