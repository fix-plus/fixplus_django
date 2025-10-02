FROM python:3.11.4

# Install system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/prod.txt && pip install weasyprint

ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/