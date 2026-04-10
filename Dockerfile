ARG PYTHON_VERSION=3.14

FROM python:${PYTHON_VERSION}-alpine

# Set up the Alpine edge repo so UV is up to date
echo "@edge https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

# Install dependencies (UV)
RUN apk add uv@edge

# Prepare work directory
RUN mkdir /markovbot
WORKDIR /markovbot

# This copies the full app (.py files and whatnot) and installs the project
COPY . /markovbot/
RUN uv sync --frozen --no-dev

# Enable the .venv so the entrypoint can know what it needs
ENV PATH="/markovbot/.venv/bin:$PATH"

ENTRYPOINT ["python3", "markovbot.py"]
