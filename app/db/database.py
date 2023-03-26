import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://dev_username:dev_password@localhost/analytics")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    return SessionLocal()

def create_tables():
    Base.metadata.create_all(checkfirst=True, bind=engine)

def drop_tables():
    Base.metadata.drop_all(bind=engine)
