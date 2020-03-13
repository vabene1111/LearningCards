FROM alpine

# Project Files and Settings

RUN mkdir /LearningCards
WORKDIR /LearningCards

ADD . /LearningCards/

RUN apk update
RUN apk upgrade
RUN apk --no-cache add \
    python3 \
    python3-dev \
    postgresql-client \
    postgresql-dev \
    build-base \
    gettext \
    jpeg-dev \
    zlib-dev

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

RUN apk del -r python3-dev

ENV PYTHONUNBUFFERED 1

# Server
EXPOSE 8080
