FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

RUN apt update; yes Yes | apt install python3-pip;

RUN /bin/bash -c "pip3 install -r requirements/requirements.txt;"
