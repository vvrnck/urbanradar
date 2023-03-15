FROM python:3.10.0a6-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ADD . /app
WORKDIR /app

# Install GDAL dependencies
RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN ["pip", "install", "--no-cache-dir", "--upgrade", "pip"]
RUN ["pip", "install", "--no-cache-dir", "--disable-pip-version-check", "-r", "requirements.txt"]


ENTRYPOINT [ "/bin/bash", "-l", "-c" ]