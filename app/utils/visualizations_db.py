from typing import Union, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import AnalyticsData, AnalyticsDataGroup, AnalyticsVisualization
from utils.visualizations import (
    create_line_chart,
    create_bar_chart,
    create_scatter_plot,
    create_pie_chart,
)

def get_or_create_visualization(
    db: Session, group: AnalyticsDataGroup, chart_type: str
) -> AnalyticsVisualization:
    visualization: Optional[AnalyticsVisualization] = (
        db.query(AnalyticsVisualization)
        .filter(AnalyticsVisualization.group_id == group.id, AnalyticsVisualization.chart_type == chart_type)
        .first()
    )

    if visualization:
        return visualization

    return generate_and_save_chart(db, group, chart_type)

def generate_and_save_chart(
    db: Session, group: AnalyticsDataGroup, chart_type: str
) -> AnalyticsVisualization:
    data: list[AnalyticsData] = db.query(AnalyticsData).filter(AnalyticsData.group_id == group.id).all()

    if chart_type == "line_chart":
        chart_data: dict[str, Union[str, list[dict[str, Union[int, float]]]]] = create_line_chart(data, f"Line Chart for Group {group.id}")
    elif chart_type == "bar_chart":
        chart_data: dict[str, Union[str, list[dict[str, Union[int, float]]]]] = create_bar_chart(data, f"Bar Chart for Group {group.id}")
    elif chart_type == "scatter_plot":
        chart_data: dict[str, Union[str, list[dict[str, Union[int, float]]]]] = create_scatter_plot(data, f"Scatter Plot for Group {group.id}")
    elif chart_type == "pie_chart":
        chart_data: dict[str, Union[str, list[dict[str, Union[str, Union[int, float]]]]]] = create_pie_chart(data, f"Pie Chart for Group {group.id}")
    else:
        raise HTTPException(status_code=400, detail="Invalid chart type")

    visualization: AnalyticsVisualization = AnalyticsVisualization(group_id=group.id, chart_type=chart_type, chart_data=chart_data)
    db.add(visualization)
    db.commit()
    return visualization
