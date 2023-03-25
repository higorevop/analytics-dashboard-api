from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AnalyticsData(Base):
    __tablename__ = 'analytics_data'
    id = Column(Integer, primary_key=True)
    review_time = Column(Integer)
    team = Column(String)
    date = Column(Date)
    merge_time = Column(Integer)
