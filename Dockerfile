FROM python:3.8-alpine

# Project Files and Settings

RUN mkdir /LearningCards
WORKDIR /LearningCards

ADD . /LearningCards/

RUN apk update
RUN apk upgrade
RUN apk add --no-cache postgresql-libs gettext
RUN apk add --no-cache --virtual .build-deps gcc musl-dev zlib-dev postgresql-dev && \
    pip install --upgrade pip &&  \
    pip install -r requirements.txt && \
    apk --purge del .build-deps

ENV PYTHONUNBUFFERED 1

# Server
EXPOSE 8080
