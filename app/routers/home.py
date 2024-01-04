from fastapi import APIRouter

from app.config import ROUTE_PREFIX_V1

from . import home

router = APIRouter()

def include_api_routes():
    ''' Include to router all api rest routes with version prefix '''
    router.include_router(home.router, prefix=ROUTE_PREFIX_V1)

include_api_routes()