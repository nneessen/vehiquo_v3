from fastapi import APIRouter

from app.config import ROUTE_PREFIX_V1

from . import home

router = APIRouter(tags=["Home"])


@router.get("/home/")
async def home():
    return {"message": "Hello World"}
