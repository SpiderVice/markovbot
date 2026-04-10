# Based on https://depot.dev/docs/container-builds/optimal-dockerfiles/python-uv-dockerfile
# This is a multistage setup.

ARG PYTHON_VERSION=3.14
ARG UV_VERSION=0.11.3

FROM python:${PYTHON_VERSION}-alpine

# Install dependencies (UV)
RUN apk add uv

# Prepare work directory
RUN mkdir /markovbot
WORKDIR /markovbot

# This copies the full app (.py files and whatnot) and installs the project
COPY . /markovbot/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENTRYPOINT ["python3", "markovbot.py"]
