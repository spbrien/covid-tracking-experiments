import io
import os
from datetime import date

import requests
import pandas as pd

from minio import Minio

minio_client = Minio(
    'minio.nobedtimes.com',
    access_key=os.environ.get('MINIO_ACCESS_KEY'),
    secret_key=os.environ.get('MINIO_SECRET_KEY')
)


def get_rate(column):
    return column.rolling(2).apply(lambda x: (x[1] - x[0]) / x[0])

def get_average_rate(column):
    return column.expanding(min_periods=1).mean()

def get_us():
    res = requests.get('https://covidtracking.com/api/v1/us/daily.json')
    data = res.json()
    df = pd.DataFrame(data)
    df = df.sort_values('date', ascending=True)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df = df.set_index('date')

    df['Death Increase Rate'] = get_rate(df['death'])
    df['Avg Death Increase Rate'] = get_average_rate(df['Death Increase Rate'])

    df['Positive Increase Rate'] = get_rate(df['positive'])
    df['Avg Positive Increase Rate'] = get_average_rate(df['Positive Increase Rate'])

    df['Testing Increase Rate'] = get_rate(df['totalTestResults'])
    df['Avg Testing Increase Rate'] = get_average_rate(df['Testing Increase Rate'])

    csv_bytes = df.to_csv().encode('utf-8')
    csv_buffer = io.BytesIO(csv_bytes)

    minio_client.put_object(
        'tracking-covid-data',
        'us-historical.csv',
        data=csv_buffer,
        length=len(csv_bytes),
        content_type='application/csv'
    )

    daily_csv_bytes = df.to_csv().encode('utf-8')
    daily_csv_buffer = io.BytesIO(csv_bytes)

    minio_client.put_object(
        'tracking-covid-data',
        'us-historical_%s.csv' % date.today(),
        data=daily_csv_buffer,
        length=len(daily_csv_bytes),
        content_type='application/csv'
    )

def get_states():
    res = requests.get('https://covidtracking.com/api/v1/states/daily.json')
    data = res.json()
    df = pd.DataFrame(data)

    csv_bytes = df.to_csv().encode('utf-8')
    csv_buffer = io.BytesIO(csv_bytes)

    minio_client.put_object(
        'tracking-covid-data',
        'states-historical.csv',
        data=csv_buffer,
        length=len(csv_bytes),
        content_type='application/csv'
    )

    daily_csv_bytes = df.to_csv().encode('utf-8')
    daily_csv_buffer = io.BytesIO(csv_bytes)

    minio_client.put_object(
        'tracking-covid-data',
        'states-historical_%s.csv' % date.today(),
        data=daily_csv_buffer,
        length=len(daily_csv_bytes),
        content_type='application/csv'
    )

get_us()
get_states()
