import pytest
from typing import Dict, Generator

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import engine
from app.main import app




SQLALCHEMY_DATABASE_URL = "sqlite:///./test/test.db"


@pytest.fixture(scope="session")
def db() -> Generator:
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
        finally:
            session.close()
                    

@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
