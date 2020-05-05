FROM python:3.7.5

# Create App directory
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY collect.py /app/collect.py

ENV MINIO_ACCESS_KEY=qUGMLsAcMZm9BG1p4b7w6JMGevtsbZZt
ENV MINIO_SECRET_KEY=f65138b3f18e417f4eb8a1764104e9cb1135964975e6df4e

RUN pip install -r requirements.txt

CMD ["python", "collect.py"]
