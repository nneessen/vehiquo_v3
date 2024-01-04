from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.database import Base

from app.dependencies import get_db

## Configure SQLite embedded for file "test.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    ''' Method for override database default configuration '''
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def configure_test_database(app):
    ''' Override default database for test embedded database '''
    
    Base.metadata.create_all(bind=engine)
    
    app.dependency_overrides[get_db] = override_get_db


def truncate_tables(tables):
    ''' Truncate rows of all input tables '''
    
    with engine.connect() as con:
        for table_name in tables:
            # Build a safe statement using SQLAlchemy text
            statement = text(f"DELETE FROM {table_name}")
            con.execute(statement)
    
    