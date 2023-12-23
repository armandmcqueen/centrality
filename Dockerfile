FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update  \
    && apt-get install -y python3.11  \
    python3.11-distutils  \
    python3.11-venv \
    python3.11-dev \
    redis-server  \
    curl \
    gcc \
    sudo \
    make

# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Copy the monorepo into the container
COPY . /centrality
WORKDIR /centrality

# Install the monorepo
RUN pip install -e ./common && \
    pip install -e ./vmagent && \
    pip install -e ./controlplane && \
    pip install -e ./rapidui

# VM agent port
EXPOSE 7777
# Control plane port
EXPOSE 8000
# RapidUI port
EXPOSE 8501