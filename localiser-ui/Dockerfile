FROM python:3-alpine
MAINTAINER gotev

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED 1

COPY . /localiser-ui/

WORKDIR /localiser-ui

# Remove existing sqlite3 file when creating docker image
RUN rm -rf db/db.sqlite3

# Setup virtualenv
RUN apk add --no-cache bash
RUN /bin/bash -c "pip3 install -r requirements.txt"

# Run
ENTRYPOINT ["/bin/bash", "./start"]

EXPOSE 8000
