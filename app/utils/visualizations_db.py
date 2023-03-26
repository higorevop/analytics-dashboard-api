from databases import Database 
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
from sqlalchemy import select

async def get_or_create_visualization(
    db: Database, group: AnalyticsDataGroup, chart_type: str
) -> AnalyticsVisualization:
    query = (
        select(AnalyticsVisualization)
        .where(
            (AnalyticsVisualization.group_id == group.id)
            & (AnalyticsVisualization.chart_type == chart_type)
        )
    )
    visualization = await db.fetch_one(query)

    if visualization:
        return visualization

    return await generate_and_save_chart(db, group, chart_type)

async def generate_and_save_chart(
    db: Database, group: AnalyticsDataGroup, chart_type: str
) -> AnalyticsVisualization:
    query = select(AnalyticsData).where(AnalyticsData.group_id == group.id)
    data = await db.fetch_all(query)

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

    visualization = AnalyticsVisualization(group_id=group.id, chart_type=chart_type, chart_data=chart_data)
    query = AnalyticsVisualization.__table__.insert().values(**visualization.dict())
    await db.execute(query)
    return visualization
