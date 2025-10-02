# This docker file is used for production
# Creating image based on official python3 image
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
RUN python -m pip install -r requirements/prod.txt && pip install ipython==8.2.0 && pip install gunicorn==20.1.0 && pip install weasyprint

ENV HOME=/app
ENV APP_HOME=/app/backend
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app && \
   groupadd -r appuser && useradd --no-log-init -r -g appuser appuser && \
    python -m pip install --upgrade pip && \
    mkdir ${APP_HOME} ${APP_HOME}/logs

WORKDIR ${APP_HOME}
EXPOSE 8000


# Install pip requirements
COPY . ${APP_HOME}