FROM python:3.12
ENV PYTHONUNBUFFERED=1
COPY . /app/

# Setup backend
WORKDIR /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /app/static/
RUN rm -rf /app/static/*
RUN python3 manage.py collectstatic --no-input
