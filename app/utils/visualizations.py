import plotly.graph_objs as go
import plotly.io as pio
import json
from db.models import AnalyticsData
from typing import List
import pandas as pd

def create_line_chart(data: List[AnalyticsData], title: str):
    df = pd.DataFrame([item.__dict__ for item in data])
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['date'], y=df['review_time'], mode='lines+markers', name='Review Time')
    )
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['merge_time'], mode='lines+markers', name='Merge Time')
    )

    fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Time')
    return json.loads(pio.to_json(fig))

def create_pie_chart(data: List[AnalyticsData], title: str):
    df = pd.DataFrame([item.__dict__ for item in data])
    team_counts = df['team'].value_counts()
    
    fig = go.Figure(
        go.Pie(labels=team_counts.index, values=team_counts.values, textinfo='label+percent')
    )

    fig.update_layout(title=title)
    return json.loads(pio.to_json(fig))


def create_bar_chart(data: List[AnalyticsData], title: str):
    df = pd.DataFrame([item.__dict__ for item in data])
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df['date'], y=df['review_time'], name='Review Time')
    )
    fig.add_trace(
        go.Bar(x=df['date'], y=df['merge_time'], name='Merge Time')
    )

    fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Time')
    return json.loads(pio.to_json(fig))


def create_scatter_plot(data: List[AnalyticsData], title: str):
    df = pd.DataFrame([item.__dict__ for item in data])
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df['review_time'], y=df['merge_time'], mode='markers', name='Data Points')
    )

    fig.update_layout(title=title, xaxis_title='Review Time', yaxis_title='Merge Time')
    return json.loads(pio.to_json(fig))