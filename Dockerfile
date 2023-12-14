FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update  \
    && apt-get install -y python3.11  \
    python3.11-distutils  \
    python3.11-venv \
    python3.11-dev \
    redis-server  \
    pipx  \
    curl \
    gcc \
    postgresql  \
    postgresql-contrib \
    sudo \
    systemctl \
    make


# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Ensure that we don't cache the code copy and install steps
RUN echo "This is an uncached step: $(date +%s)"

# Copy the monorepo into the container
COPY . /centrality
WORKDIR /centrality

# Install the monorepo
RUN cd /centrality && pip install -e ./common && \
    pip install -e ./vmagent && \
    pip install -e ./controlplane

EXPOSE 8000