from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import AnalyticsData, AnalyticsDataGroup
from utils.analytics import get_summary_statistics

router = APIRouter()

@router.get("/{group_id}/summary")
def get_group_summary(group_id: int, db: Session = Depends(get_db)):
    group = db.query(AnalyticsDataGroup).get(group_id)

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    data = db.query(AnalyticsData).filter(AnalyticsData.group_id == group_id).all()
    summary = get_summary_statistics(data)

    return summary
