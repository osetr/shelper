FROM ubuntu

RUN apt update; yes Yes | apt install python3-pip;

COPY . ./app

ENV FLASK_APP main.py

ENV FLASK_ENV development

WORKDIR /app/

RUN /bin/bash -c "pip3 install -r requirements/requirements.txt;"
