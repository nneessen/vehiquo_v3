import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db" #^ FOR PRODUCTION
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  #! FOR TESTING ONLY

engine = create_engine(
    os.getenv("DB_URL", SQLALCHEMY_DATABASE_URL),
    # echo=True,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
