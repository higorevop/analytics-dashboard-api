import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import AnalyticsData, Base 

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://dev_username:dev_password@localhost/analitics")

engine = create_engine(DATABASE_URL)
Base = declarative_base() 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    return SessionLocal()

def create_tables():
    Base.metadata.create_all(checkfirst=True, bind=engine)

def drop_tables():
    Base.metadata.drop_all(bind=engine)

__all__ = ["SessionLocal"]
