from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import AnalyticsDataGroup

router = APIRouter()

@router.get("/{group_id}/summary")
def get_group_summary(
    group_id: int,
    db: Session = Depends(get_db),
):
    """
    Get Group Summary

    Get a summary statistics for a specific analytics data group.
    """
    group = db.query(AnalyticsDataGroup).get(group_id)

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    summary = {
        "review_time": {
            "mean": group.mean_review_time,
            "median": group.median_review_time,
            "mode": group.mode_review_time,
        },
        "merge_time": {
            "mean": group.mean_merge_time,
            "median": group.median_merge_time,
            "mode": group.mode_merge_time,
        },
    }
    return summary