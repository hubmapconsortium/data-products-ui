FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get -y install \
    libmemcached-dev \
    python3 \
    python3-dev \
    python3-pip \
    python-is-python3 \
 && rm -rf /var/cache/apt/*

## Python packages
COPY requirements.txt /opt/requirements.txt
COPY data /opt
RUN pip3 install -r /opt/requirements.txt \
 && rm -rf /root/.cache/pip
