# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y \
        make linux-headers-generic libffi-dev libjpeg-dev libz-dev \
        postgresql-server-dev-all gcc python3-dev musl-dev libpq-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy local code to the container image.
ENV APP_HOME /app
ENV JSON_RESPONSE='{"data": [], "errors": []}'
# ENV GOOGLE_APPLICATION_CREDENTIALS="./service-account.json"
# ENV PROJECT_ID="crimeradar-dev"
# ENV SECRET_ID="firebase-crimeradar"

WORKDIR $APP_HOME
COPY . ./
# Make the script executable
RUN chmod +x db_migration.sh 

# Install production dependencies.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

#CMD exec gunicorn --bind :8000 --workers 1 --threads 8 --timeout 0 wsgi:g_app
CMD ["sh", "-c", "./db_migration.sh && ./start.sh"]