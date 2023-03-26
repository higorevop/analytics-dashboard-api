
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.database import engine
from db.database import get_db
from db.database import Base
from db.models import AnalyticsDataGroup
Base.metadata.create_all(bind=engine)
from utils.visualizations_db import get_or_create_visualization

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException, Request, Path
# ... (restante das importações)

@router.get("/{group_id}/visualizations/{chart_type}")
def get_visualization(
        group_id: int,
        request: Request,
        db: Session = Depends(get_db),
        chart_type: str = Path(..., description="Type of chart to retrieve (line_chart, bar_chart, scatter_plot or pie_chart)"),

):
    """
    Get Visualization

    Retrieve a visualization for a specific analytics data group.

    Available chart types:
    - line_chart: Line chart showing review time and merge time over dates.
    - bar_chart: Bar chart showing review time and merge time over dates.
    - scatter_plot: Scatter plot showing the relationship between review time and merge time.
    - pie_chart: Pie chart showing the distribution of team contributions.

    The visualization will be created if it does not exist, and a shareable URL will be provided.
    """
    group = db.get(AnalyticsDataGroup, group_id)

    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    visualization = get_or_create_visualization(db, group, chart_type)
    share_url = f"{request.url_for('get_visualization', group_id=group_id, chart_type=chart_type)}"
    return {"chart_data": visualization.chart_data, "share_url": share_url}