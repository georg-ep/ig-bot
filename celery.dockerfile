FROM python:3.9
LABEL MAINTAINER="Pixelfield, s.r.o"
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y dist-upgrade
COPY ./requirements.txt /requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

WORKDIR /app
COPY ./app /app
COPY .env /.env
COPY ./scripts /scripts

# RUN chmod +x scripts/celery_run.sh
# RUN chmod +x scripts/celery_start.sh

CMD ["sh", "/scripts/celery_run.sh"]
