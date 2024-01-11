from fastapi import APIRouter

from app.config import ROUTE_PREFIX_V1

from . import users, home, units, stores

router = APIRouter()

def include_api_routes():
    ''' Include to router all api rest routes with version prefix '''
    router.include_router(users.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(home.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(units.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(stores.router, prefix=ROUTE_PREFIX_V1)

include_api_routes()