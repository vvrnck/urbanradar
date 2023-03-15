# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y \
        make linux-headers-generic libffi-dev libjpeg-dev libz-dev \
        postgresql-server-dev-13 gcc python3-dev musl-dev libpq-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy local code to the container image.
ENV APP_HOME /app
ENV JSON_RESPONSE='{"data": [], "errors": []}'
ENV GOOGLE_APPLICATION_CREDENTIALS="./crimeradar-2b2f638c9f6d.json"
ENV PROJECT_ID="crimeradar"
ENV SECRET_ID="firebase-crimeradar"

WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN ["pip", "install", "--no-cache-dir", "--upgrade", "pip"]
RUN pip install psycopg2
RUN ["pip", "install", "--no-cache-dir", "--disable-pip-version-check", "-r", "requirements.txt"]
RUN pip install gunicorn

CMD exec gunicorn --bind :8000 --workers 1 --threads 8 --timeout 0 wsgi:g_app