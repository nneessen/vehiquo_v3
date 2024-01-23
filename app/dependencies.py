import os
import secrets

from jose import jwt, JWTError
from fastapi import Header, HTTPException

from app.database import SessionLocal

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"


def decode(token):
    striped_token = token.replace("Bearer ", "")
    return jwt.decode(token, "secret", algorithm="HS256")


def encode():
    return jwt.encode({"some": "payload"}, "secret", algorithm="HS256")


def get_db():
    """Method for configure database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_token_header(x_token: str = Header(...)):
    """
    Get token from header

    Args:
        x_token (str): Token from header

    Raises:
        HTTPException: If token is invalid
    """
    payload = decode(x_token)
    username: str = payload.get("email")
    if username == None:
        raise HTTPException(status_code=403, detail="Unauthorized")


async def get_query_token(token: str):
    """
    Get token from query

    Args:
        token (str): Token from query

    Raises:
        HTTPException: If token is invalid
    """
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")


def generate_secret_key():
    return secrets.token_hex(32)
