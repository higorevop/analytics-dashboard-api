from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from db.database import Base

class AnalyticsDataGroup(Base):
    __tablename__ = "analytics_data_group"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(Date)
    mean_review_time = Column(Float)
    median_review_time = Column(Float)
    mode_review_time = Column(Float)
    mean_merge_time = Column(Float)
    median_merge_time = Column(Float)
    mode_merge_time = Column(Float)

    class Config:
        orm_mode = True



class AnalyticsData(Base):
    __tablename__ = "analytics_data"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    review_time = Column(Integer)
    team = Column(String)
    date = Column(Date)
    merge_time = Column(Integer)
    group_id = Column(Integer, ForeignKey("analytics_data_group.id"))

    class Config:
        orm_mode = True
