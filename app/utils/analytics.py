from typing import List
from db.models import AnalyticsData, AnalyticsDataGroup
from sqlalchemy.orm import Session
import pandas as pd

def calculate_and_store_summary(db: Session, group: AnalyticsDataGroup, data: List[AnalyticsData]):
    df = pd.DataFrame([{
        'review_time': item.review_time,
        'merge_time': item.merge_time
    } for item in data])

    group.mean_review_time = df["review_time"].mean().item()
    group.median_review_time = df["review_time"].median().item()
    group.mode_review_time = df["review_time"].mode()[0].item()

    group.mean_merge_time = df["merge_time"].mean().item()
    group.median_merge_time = df["merge_time"].median().item()
    group.mode_merge_time = df["merge_time"].mode()[0].item()

    db.add(group)
    db.commit()

