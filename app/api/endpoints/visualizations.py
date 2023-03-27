from fastapi import APIRouter, Depends, HTTPException, Request, Path
from sqlalchemy.orm import Session
from sqlalchemy import select
from databases import Database
from db.database import get_db
from db.models import AnalyticsDataGroup
from utils.visualizations_db import get_or_create_visualization

router = APIRouter()


@router.get("/{group_id}/visualizations/{chart_type}")
async def get_visualization(
    group_id: int,
    request: Request,
    db: Database = Depends(get_db),
    chart_type: str = Path(
        ...,
        description="Type of chart to retrieve (bar_chart, scatter_plot or pie_chart)",
    ),
) -> dict:
    """
    Get Visualization

    Retrieve a visualization for a specific analytics data group.

    Available chart types:
    - bar_chart: Bar chart showing merge time over dates.
    - scatter_plot: Scatter plot showing the relationship between review time and merge time.
    - pie_chart: Pie chart showing the distribution of team contributions.

    The visualization will be created if it does not exist, and a shareable URL will be provided.
    """
    query = select(AnalyticsDataGroup).where(AnalyticsDataGroup.id == group_id)
    group = await db.fetch_one(query)

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    visualization = await get_or_create_visualization(db, group, chart_type)
    share_url = f"{request.url_for('get_visualization', group_id=group_id, chart_type=chart_type)}"
    return {"chart_data": visualization.chart_data, "share_url": share_url}
