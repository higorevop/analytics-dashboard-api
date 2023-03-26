from databases import Database 
from typing import List
from db.models import AnalyticsData, AnalyticsDataGroup
import pandas as pd


async def calculate_and_store_summary(db: Database, group: AnalyticsDataGroup, data: List[AnalyticsData]) -> None:
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

    query = (
        AnalyticsDataGroup.__table__.update()
        .where(AnalyticsDataGroup.id == group.id)
        .values(
            mean_review_time=group.mean_review_time,
            median_review_time=group.median_review_time,
            mode_review_time=group.mode_review_time,
            mean_merge_time=group.mean_merge_time,
            median_merge_time=group.median_merge_time,
            mode_merge_time=group.mode_merge_time,
        )
    )
    await db.execute(query)
