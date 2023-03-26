from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.api.schemas.analytics_data import AnalyticsDataCreate
from app.models import AnalyticsData

def create_analytics_data(db: Session, data: AnalyticsDataCreate):
    db_data = AnalyticsData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
