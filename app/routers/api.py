from fastapi import APIRouter, Depends

from app.config import ROUTE_PREFIX_V1
from app.routers.security.dependencies import CURRENT_USER, SESSION

from . import home, stores, units, users, vehicles

router = APIRouter()


def include_api_routes():
    """Include to router all api rest routes with version prefix"""
    router.include_router(users.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(home.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(units.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(stores.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(vehicles.router, prefix=ROUTE_PREFIX_V1)


include_api_routes()
