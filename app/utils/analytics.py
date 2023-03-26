import pandas as pd
from db.models import AnalyticsData
from typing import List

def get_summary_statistics(data: List[AnalyticsData]) -> pd.DataFrame:
    df = pd.DataFrame([item.__dict__ for item in data])

    mean_review_time = df["review_time"].mean()
    median_review_time = df["review_time"].median()
    mode_review_time = df["review_time"].mode()[0]

    mean_merge_time = df["merge_time"].mean()
    median_merge_time = df["merge_time"].median()
    mode_merge_time = df["merge_time"].mode()[0]

    statistics = pd.DataFrame(
        {
            "review_time": {
                "mean": mean_review_time,
                "median": median_review_time,
                "mode": mode_review_time,
            },
            "merge_time": {
                "mean": mean_merge_time,
                "median": median_merge_time,
                "mode": mode_merge_time,
            },
        }
    )

    return statistics
