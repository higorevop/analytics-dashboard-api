from datetime import date
from sqlalchemy import Column, Integer, String, Date
from db.database import Base

class AnalyticsData(Base):
    __tablename__ = "analytics_data"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    review_time = Column(Integer)
    team = Column(String)
    date = Column(Date)
    merge_time = Column(Integer)

    class Config:
        orm_mode = True
