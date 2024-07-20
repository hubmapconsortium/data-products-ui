FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get -y install \
    libmemcached-dev \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    python-is-python3 \
 && rm -rf /var/cache/apt/*

## Python packages
COPY requirements.txt /opt/requirements.txt
COPY data /opt
RUN python3 -m venv /opt/venv \
 && . /opt/venv/bin/activate \
 && pip install -U pip setuptools wheel \
 && pip install -r /opt/requirements.txt \
 && rm -rf /root/.cache/pip \
 && echo '. /opt/venv/bin/activate' >> /etc/bash.bashrc
