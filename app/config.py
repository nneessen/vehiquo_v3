from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Authorization"

config = Config(".env")

ROUTE_PREFIX_V1 = "/v1"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)
