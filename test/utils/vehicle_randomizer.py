import random
import string
from typing import Dict
from test.utils.vehicle_config import vehicle_configs


def random_year() -> int:
    return random.randint(2000, 2024)

def random_make() -> str:
    return random.choice(list(vehicle_configs.keys()))

def random_model(make: str) -> str:
    return random.choice(vehicle_configs[make]["models"])

def random_trim(make: str, model: str) -> str:
    if make in vehicle_configs:
        if model in vehicle_configs[make]["models"]:
            return random.choice(vehicle_configs[make]["trims"])
        else:
            raise ValueError(f"Model {model} not found in {make} vehicle configs.")
    else:
        raise ValueError(f"Make {make} not found in vehicle configs.")

def random_mileage() -> int:
    return random.randint(1000, 60000)

def random_color() -> str:
    return random.choice(["red", "blue", "green", "black", "white", "silver"])

def random_vin() -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=17))

def random_drivetrain() -> str:
    return random.choice(["AWD", "FWD", "RWD"])

def random_transmission() -> str:
    return random.choice(["automatic", "manual"])

def random_transmission_type() -> str:
    return random.choice(["automatic", "manual"])

def random_transmission_speeds() -> int:
    return random.randint(4, 9)

def random_highway_mileage() -> int:
    return random.randint(20, 40)

def random_city_mileage() -> int:
    return random.randint(10, 30)

def random_engine_cylinders() -> int:
    return random.randint(4, 8)

def random_category() -> str:
    return random.choice(["sedan", "coupe", "hatchback", "truck", "suv"])

def random_msrp() -> int:
    return random.randint(22500, 50000)


def create_random_vehicle_data() -> Dict[str, str]:
    make = random_make()
    model = random_model(make)
    trim = random_trim(make, model)
    return {
        "year": random_year(),
        "make": make,
        "model": model,
        "trim": trim,
        "mileage": random_mileage(),
        "color": random_color(),
        "vin": random_vin(),
        "drivetrain": random_drivetrain(),
        "transmission": random_transmission(),
        "transmission_type": random_transmission_type(),
        "transmission_speeds": random_transmission_speeds(),
        "highway_mileage": random_highway_mileage(),
        "city_mileage": random_city_mileage(),
        "engine_cylinders": random_engine_cylinders(),
        "category": random_category(),
        "msrp": random_msrp(),
    }
    
