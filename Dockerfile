FROM ubuntu:18.04

LABEL maintainer="github.com/hb-i"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev curl

WORKDIR /app

# Install required packages
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
