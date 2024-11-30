FROM python:3.11.4

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install -r requirements/prod.txt

ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Get the django project into the docker container
RUN mkdir /app
WORKDIR /app
ADD ./ /app/