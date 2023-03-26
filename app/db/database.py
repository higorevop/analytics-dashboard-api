import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from typing import Generator

Base = declarative_base()

load_dotenv()

DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql://dev_username:dev_password@localhost/analytics")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables() -> None:
    Base.metadata.create_all(checkfirst=True, bind=engine)

def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)
