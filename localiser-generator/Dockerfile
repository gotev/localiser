FROM python:3-alpine
MAINTAINER gotev

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED 1

COPY . /localiser-generator/

WORKDIR /localiser-generator

# Setup virtualenv
RUN apk add --no-cache bash
RUN /bin/bash -c "pip3 install -r requirements.txt"

# Run
ENTRYPOINT ["python3", "localiser-generator.py", "db.sqlite3"]
