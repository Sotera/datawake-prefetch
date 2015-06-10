FROM ubuntu:14.04

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install \
  g++ \
  git \
  python-dev \
  python-pip

RUN pip install \
  tangelo \
  HTMLParser

# setup tangelo conf and entry point for container
RUN adduser  --no-create-home --disabled-password --disabled-login --gecos "" tangelo

ENV PYTHONPATH /usr/local/share/tangelo/web:$PYTHONPATH

WORKDIR /usr/local/share/tangelo/web
