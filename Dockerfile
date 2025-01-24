FROM python:3.12
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y install gdal-bin
RUN pip install --upgrade pip

COPY . /app/

# Setup backend
WORKDIR /app/
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN mkdir -p /app/static/
RUN rm -rf /app/static/*
RUN python3 manage.py collectstatic --no-input
