import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime
from minio import Minio

minio_client = Minio(
    'minio.nobedtimes.com',
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_KEY')
)

data = minio_client.get_object(
    'tracking-covid-data',
    'states-historical.csv'
)
df = pd.read_csv(data)
df = df.drop(columns=[df.columns[0]])
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
df = df.sort_values('date', ascending=True)
mi = df[df['state'] == 'WI']

mi['10 Day Average'] = mi['positiveIncrease'].rolling(window=10).mean()
mi['10 Day Death Average'] = mi['deathIncrease'].rolling(window=10).mean()

print(mi)

cases = [
    go.Bar(
        legendgroup="New Cases",
        x=mi['date'], # assign x as the dataframe column 'x'
        y=mi['positiveIncrease'],
        name='Daily New Cases'
    ),
    go.Scatter(
        legendgroup="New Cases",
        x=mi['date'],
        y=mi['10 Day Average'],
        mode='lines+markers',
        name='10 Day Average'
    ),
]

testing = [
    go.Bar(
        legendgroup="New Deaths",
        x=mi['date'], # assign x as the dataframe column 'x'
        y=mi['deathIncrease'],
        name='Daily New Deaths'
    ),
    go.Scatter(
        legendgroup="New Deaths",
        x=mi['date'],
        y=mi['10 Day Death Average'],
        mode='lines+markers',
        name='10 Day Deaths Average'
    ),
]

positive = go.Scatter(
    legendgroup="Totals",
    x=mi['date'],
    y=mi['positive'],
    mode='lines+markers',
    name='Positive Cases'
)

deaths = go.Scatter(
    legendgroup="Totals",
    x=mi['date'],
    y=mi['death'],
    mode='lines+markers',
    name='Deaths'
)

output = make_subplots(
    rows=1,
    cols=1,
)

output.add_trace(cases[0], row=1, col=1)
output.add_trace(cases[1], row=1, col=1)
# output.add_trace(testing[0], row=1, col=2)
# output.add_trace(testing[1], row=1, col=2)
# output.add_trace(positive, row=2, col=1)
# output.add_trace(deaths, row=2, col=2)
output.update_layout(
    title="Wisconsin Covid-19 Daily New Cases",
    template='seaborn',
    annotations=[
        dict(
            x=datetime.strptime('2020-04-07', '%Y-%m-%d'),
            y=138,
            xref="x",
            yref="y",
            text="Wisconsin Primary Voting",
            showarrow=True,
            ax=0,
            ay=-110,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
            ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        ),
        dict(
            x=datetime.strptime('2020-04-19', '%Y-%m-%d'),
            y=146.7,
            xref="x",
            yref="y",
            text="Median Inucbation Period",
            showarrow=True,
            ax=0,
            ay=-110,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
            ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        ),
        dict(
            x=datetime.strptime('2020-04-22', '%Y-%m-%d'),
            y=225,
            xref="x",
            yref="y",
            text="Testing Turnaround",
            showarrow=True,
            ax=0,
            ay=-110,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
            ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )
    ]
)
output.show()
