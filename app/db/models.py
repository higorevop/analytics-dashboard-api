from typing import List
from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime


class AnalyticsDataGroup(Base):
    __tablename__ = "analytics_data_group"
    __table_args__ = {'extend_existing': True}
    id: int = Column(Integer, primary_key=True, index=True)
    created_at: Date = Column(Date)
    mean_review_time: float = Column(Float)
    median_review_time: float = Column(Float)
    mode_review_time: float = Column(Float)
    mean_merge_time: float = Column(Float)
    median_merge_time: float = Column(Float)
    mode_merge_time: float = Column(Float)
    visualizations = relationship("AnalyticsVisualization", back_populates="group", cascade="all, delete-orphan") # type: ignore

    class Config:
        orm_mode = True


class AnalyticsData(Base):
    __tablename__ = "analytics_data"
    __table_args__ = {'extend_existing': True}
    id: int = Column(Integer, primary_key=True, index=True)
    review_time: int = Column(Integer, nullable=False)
    team: str = Column(String, nullable=False)
    date: Date = Column(Date, nullable=False)
    merge_time: int = Column(Integer, nullable=False)
    group_id: int = Column(Integer, ForeignKey("analytics_data_group.id"))

    class Config:
        orm_mode = True


class AnalyticsVisualization(Base):
    __tablename__ = "analytics_visualization"

    id: int = Column(Integer, primary_key=True, index=True)
    group_id: int = Column(Integer, ForeignKey("analytics_data_group.id"), nullable=False)
    group = relationship("AnalyticsDataGroup", back_populates="visualizations")
    chart_type: str = Column(String, nullable=False)
    chart_data: dict = Column(JSON, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
